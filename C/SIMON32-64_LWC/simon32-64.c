/*
  File name: simon32-64.c
  Author: Cesar Cruz
  Project: SIMON32-64_LWC
*/

#include <stdio.h>
#include <stdlib.h>

#define KEY_SIZE 64
#define N 16
#define M 4
#define T 32
#define J 0

int** key_expansion(int* key);

int** init_keys(int* key_words);

/* Auxiliar functions */
int* xor(int* arr1, int* arr2, int size);
int* left_shift(int* array, int times);
int* right_shift(int* array, int times);
int* not(int* array, int size);
int* z_expansion(int z, int size);
int* copy_array(int* origin, int size);
int* get_chunk(int* array, int begin, int final);
void print_array(int*array, int size);

int main() {
	int key[KEY_SIZE] = {0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0,
		0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0 ,0,
		0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0 ,0, 0,
		0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0};

  int plaintext[N * 2] = {0,1,1,0, 0,1,0,1, 0,1,1,0, 0,1,0,1,
      0,1,1,0, 1,0,0,0, 0,1,1,1, 0,1,1,1};

  int** keys = key_expansion(key);

  for (int i = 0; i < T; i++) {
    printf("%d ->", i);
    print_array(keys[i], N);
  }
	
}

int** key_expansion(int* key) {
	int** keys = (int **) malloc(sizeof(int) * 128);
  int* tmp = malloc(sizeof(int) * N);
  int* tmp2 = malloc(sizeof(int) * N);
  int three[N] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1};
  int z[62] = {1,1,1,1,1,0,1,0,0,0,1,0,0,1,0,1,0,1,1,0,0,0,0,1,1,1,0,0,1,1,0,1,1,1,1,1,0,1,0,0,0,1,0,0,1,0,1,0,1,1,0,0,0,0,1,1,1,0,0,1,1,0};

  keys = init_keys(key);

  for (int i = M; i < T; i++) {
    
    tmp = right_shift(keys[i - 1], 3);    
    tmp = xor(tmp, keys[i - 3], N);
    
    tmp2 = copy_array(tmp, N);
    tmp = right_shift(tmp, 1);
    tmp = xor(tmp, tmp2, N);
    
    tmp2 = not(keys[i - M], N);
    tmp = xor(tmp, tmp2, N);
    tmp = xor(tmp, z_expansion(z[i - M], N), N);
    tmp = xor(tmp, three, N);    

    keys[i] = copy_array(tmp, N);
  }  
  
  return keys;
}

int** init_keys(int* key_words) {
  int** keys = (int **) malloc(sizeof(int) * 128);

  for (int i = M; i > 0; i--) {
    keys[M - i] = get_chunk(key_words, 16 * (i - 1), (i * 16) - 1);
  }

  return keys;
}


// AUXILIAR FUNCTIONS //
/* Function that makes a X-OR operation between two arrays (arr1, arr2) */
int* xor(int* arr1, int* arr2, int size) {
  int* tmp = malloc(sizeof(int) * size);
  
  for (int i = 0; i < size; i++) {    
    tmp[i] = arr1[i] != arr2[i];
  }

  return tmp;
}

int* left_shift(int* array, int times) {
  int i = 0, j = 0;

  /* Shift to the left of an array */
  for (j = 0; j < times; j++) {
    int pos0 = array[0];
    for (i = 0; i < N - 1; i++) {
      array[i] = array[i + 1];
    }

    array[i] = pos0;
  }
  

  return array;
}

int* right_shift(int* array, int times) {
  int i = 0, j = 0;
  int* tmp = malloc(sizeof(int) * N);
  tmp = copy_array(array, N);

  /* Shift to the left of an array */
  for (j = 0; j < times; j++) {
    int posN = tmp[N - 1];
    for (i = N - 1; i > 0; i--) {
      tmp[i] = tmp[i - 1];
    }

    tmp[0] = posN;
  }
  

  return tmp;
}

int* not(int* array, int size) {
  int* tmp = malloc(sizeof(int) * size);
  tmp = copy_array(array, size);

  for (int i = 0; i < size; i++) {
    tmp[i] = !tmp[i];
  }

  return tmp;
}

int* z_expansion(int z, int size) {
  int* tmp = malloc(sizeof(int) * size);
  int i = 0;
  for (i = 0; i < size - 1; i++) {
    tmp[i] = 0;
  }

  tmp[i] = z;

  return tmp;
}

int* copy_array(int* origin, int size) {
  int* tmp = malloc(sizeof(int) * size);
  
  for (int i = 0; i < size; i++) {
    tmp[i] = origin[i];
  }

  return tmp;
}

/* Function that gets a chunk of an array, from one position (begin) to another (final) */
int* get_chunk(int* array, int begin, int final) {  
  int size = final - begin;
  int* chunk = malloc(sizeof(int) * size);

  for (int i = begin, j = 0; i < final; i++, j++) {
    chunk[j] = array[i];    
  }  

  return chunk;
}

/* Function that prints an array on account of the size */
void print_array(int* array, int size) {
  for (int j = 0; j < size; j++) {
    printf("%d ", array[j]);
  }
  printf("\n");
}
