#include <stdio.h>

void bubble(int * a, int n) {
  int i = 0, j;

  while(i < n - 1) {
    j=0;
    while (j < n - i - 1) {
      if (a[j] > a[j + 1]) {
        //SWAP
        a[j] = a[j] + a[j + 1];
        a[j + 1] = a[j] - a[j + 1];
        a[j] = a[j] - a[j + 1];
      }
      j++;
    }
    i++;
  }
}

int main() {
  int arr[] = {3, 1, 2, 7, 9, 4};
  //length of arr
  int n = sizeof(arr)/sizeof(arr[0]);
  bubble(arr, 6);

  for (int i = 0; i < n; i++) {
    printf("%d ", arr[i]);
  }

  printf("\n");
  
  return 0;
}