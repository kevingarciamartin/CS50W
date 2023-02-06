#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    // Check command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE");
        return 1;
    }

    // Open memory card
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    int jpegCount = -1;
    FILE *img = NULL;
    char *filename = malloc(8);
    uint8_t buffer[BLOCK_SIZE];

    // Repeat until end of card:
    // Read 512 bytes into a buffer
    while (fread(buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        // If start of new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If previous JPEG open
            if (img != NULL)
            {
                fclose(img);
            }
            // Open JPEG
            jpegCount++;
            sprintf(filename, "%03i.jpg", jpegCount);
            img = fopen(filename, "w");
        }
        // Else
        else
        {
            // If already found JPEG
            if (img != NULL)
            {
                fwrite(buffer, 1, BLOCK_SIZE, img);
            }
        }
    }
    // Close any remaining files
    fclose(file);
    fclose(img);
    free(filename);

    return 0;
}