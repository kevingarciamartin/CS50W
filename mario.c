#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt for height
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // Print pyramids
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < 2 * height; j++)
        {
            // Right-aligned pyramid
            if (j >= height - 1 - i)
            {
                // Left-aligned pyramid
                if (j > height + i)
                {
                    break;
                }
                printf("#");
            }
            else
            {
                printf(" ");
            }

            // Make gap between pyramids
            if (j == height - 1)
            {
                for (int k = 0; k < 2; k++)
                {
                    printf(" ");
                }
            }
        }
        printf("\n");
    }
}