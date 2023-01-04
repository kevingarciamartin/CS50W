#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    // TODO: Prompt for start size
    int start;
    do
    {
        start = get_int("Starting population size: ");
    }
    while (start < 9);

    // TODO: Prompt for end size
    int end;
    do
    {
        end = get_int("Ending population size: ");
    }
    while (end < start);

    // TODO: Calculate number of years until we reach threshold
    int n = 0;
    int pop = start;
    while (pop < end)
    {
        pop = pop + floor(pop/3) - floor(pop/4);
        n++;
    }

    // TODO: Print number of years
    printf("Years: %i\n", n);
}
