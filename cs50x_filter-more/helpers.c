#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round(((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0));
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int j = 0; j < height; j++) // Move down the j-axis
    {
        for (int i = 0; i < width / 2; i++) // Move right along the i-axis from left
        {
            RGBTRIPLE copy_left = image[j][i];
            image[j][i] = image[j][width - i - 1];
            image[j][width - i - 1] = copy_left;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{   //create a copy to avoid overwriting
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    //iterate through the picture
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int count = 0;
            int sumBlue = 0;
            int sumGreen = 0;
            int sumRed = 0;
            //iterate through surrounding pixels
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    // Check if the neighboring pixel is in scope of the picture
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        sumBlue += copy[ni][nj].rgbtBlue;
                        sumGreen += copy[ni][nj].rgbtGreen;
                        sumRed += copy[ni][nj].rgbtRed;
                        count++;
                    }
                }
            }

            // Calculate the average values
            image[i][j].rgbtBlue = round(sumBlue / (float)count);
            image[i][j].rgbtGreen = round(sumGreen / (float)count);
            image[i][j].rgbtRed = round(sumRed / (float)count);
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int ni = 0;
    int nj = 0;

    //initialize kernels
    int gx_kernel[3][3] = {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };
    int gy_kernel[3][3] = {
        {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1}
    };

     //create a copy to avoid overwriting
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    //iterate through the picture
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //reset accumulators
            int gy_Blue = 0;
            int gy_Green = 0;
            int gy_Red = 0;
            int gx_Blue = 0;
            int gx_Green = 0;
            int gx_Red = 0;

            //Initialize copy of current picture 3x3 Grid
            RGBTRIPLE screenshot[3][3];

            //iterate through surrounding pixels
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    ni = i + di;
                    nj = j + dj;

                    // Check if the neighboring pixel is in scope of the picture
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        screenshot[di + 1][dj + 1] = copy[ni][nj];
                    }
                    else
                    {
                        screenshot[di + 1][dj + 1].rgbtBlue = 0;
                        screenshot[di + 1][dj + 1].rgbtGreen = 0;
                        screenshot[di + 1][dj + 1].rgbtRed = 0;
                    }
                }
            }
             //apply Sobel Operator

            for (int k = 0; k < 3; k++)
            {
                for (int l = 0; l < 3; l++)
                {
                    gx_Blue += (screenshot[k][l].rgbtBlue * gx_kernel[k][l]);
                    gx_Green += (screenshot[k][l].rgbtGreen * gx_kernel[k][l]);
                    gx_Red += (screenshot[k][l].rgbtRed * gx_kernel[k][l]);

                    gy_Blue += (screenshot[k][l].rgbtBlue * gy_kernel[k][l]);
                    gy_Green += (screenshot[k][l].rgbtGreen * gy_kernel[k][l]);
                    gy_Red += (screenshot[k][l].rgbtRed * gy_kernel[k][l]);
                }
            }

            int blue = round(sqrt(gx_Blue * gx_Blue  + gy_Blue * gy_Blue));
            int green = round(sqrt(gx_Green * gx_Green  + gy_Green * gy_Green));
            int red = round(sqrt(gx_Red * gx_Red  + gy_Red * gy_Red));

            //Clamping the values
            image[i][j].rgbtBlue = (blue > 255) ? 255 : blue;
            image[i][j].rgbtGreen = (green > 255) ? 255 : green;
            image[i][j].rgbtRed = (red > 255) ? 255 : red;
        }
    }
    return;
}
