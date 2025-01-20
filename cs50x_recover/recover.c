#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf ("Only one command-line argument accepted\n");
        return 1;
    }
    FILE* inptr = fopen (argv[1], "r"); //Open input for reading.
    if (inptr == NULL)
    {
        printf("File cannot be opened\n");
        return 1;
    }

    //Defining a 8 bit values
    typedef uint8_t byte;

    //Defining 512 byte chunk
    typedef struct{
        byte data[512];
    } chunk;

    //Creating reading buffer size of one chunk
    chunk read_buffer[1];

    //Checking for EOF
    size_t bytes_read;

    //File name process
    const int n = 7;
    char output_file_name[n];
    int counter = 0;
    FILE* outptr = NULL;

//Copy process
    while((bytes_read = fread(read_buffer, sizeof(chunk), 1, inptr)) > 0)
    {
        //Checking for JPEG
        if (read_buffer[0].data[0] == 0xff && read_buffer[0].data[1] == 0xd8 &&
            read_buffer[0].data[2] == 0xff && (read_buffer[0].data[3] & 0xf0) == 0xe0)
        {
            if (outptr != NULL)
                fclose(outptr);

            //Create a new JPEG file for writing
            sprintf(output_file_name, "%03d.jpg", counter++);
            outptr = fopen(output_file_name, "w");
            if (outptr == NULL)
            {
                printf("File cannot be opened\n");
                return 1;
            }
        }
        if (outptr != NULL)
            fwrite(read_buffer, sizeof(chunk), 1, outptr);
    }
    if (outptr != NULL)
        fclose(outptr);

fclose(inptr);

return 0;
}
