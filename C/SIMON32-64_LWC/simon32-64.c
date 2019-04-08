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
int* cipher(int* plaintext, int** keys);
int* decipher(int* ciphertext, int** keys);
int** init_keys(int* key_words);

/* Auxiliar functions */
int* xor(int* arr1, int* arr2, int size);
int* and(int* arr1, int* arr2, int size);
int* left_shift(int* array, int times);
int* right_shift(int* array, int times);
int* not(int* array, int size);
int* z_expansion(int z, int size);
int* copy_array(int* origin, int size);
int* get_chunk(int* array, int begin, int final);
int* join_chunks(int* ch1, int* ch2, int s1, int s2);
void print_array(int*array, int size);

int main() {
	int key[KEY_SIZE] = {0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0,
		0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0 ,0,
		0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0 ,0, 0,
		0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0};

  int plaintext[N * 2] = {0,1,1,0, 0,1,0,1, 0,1,1,0, 0,1,0,1,
      0,1,1,0, 1,0,0,0, 0,1,1,1, 0,1,1,1};

  int* ciphertext = malloc(sizeof(int) * (2 * N));
  int* recovertext = malloc(sizeof(int) * (2 * N));

  int** keys = key_expansion(key);

  ciphertext = cipher(plaintext, keys);
  print_array(ciphertext, N * 2);

  recovertext = decipher(ciphertext, keys);
  print_array(recovertext, N * 2);
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

int* cipher(int* plaintext, int** keys) {
  int* x = malloc(sizeof(int) * N);
  int* y = malloc(sizeof(int) * N);
  int* tmp = malloc(sizeof(int) * N);
  int* tmp2 = malloc(sizeof(int) * N);
  
  /* X and Y */
  x = get_chunk(plaintext, 0, 16);
  y = get_chunk(plaintext, 16, 32);
  
  for (int i = 0; i < T; i++) {    
    tmp = copy_array(x, N);
    tmp2 = left_shift(x, 1);
    tmp2 = and(tmp2, left_shift(x, 8), N);
    tmp2 = xor(y, tmp2, N);
    tmp2 = xor(tmp2, left_shift(x, 2), N);
    x = xor(tmp2, keys[i], N);
    y = copy_array(tmp, N);    
  }

  return join_chunks(x, y, N, N);
}

int* decipher(int* ciphertext, int** keys) {
  int* x = malloc(sizeof(int) * N);
  int* y = malloc(sizeof(int) * N);
  int* tmp = malloc(sizeof(int) * N);
  int* tmp2 = malloc(sizeof(int) * N);
  
  /* X and Y */
  x = get_chunk(ciphertext, 0, 16);
  y = get_chunk(ciphertext, 16, 32);
  
  for (int i = 0; i < T; i++) {    
    tmp = copy_array(y, N);
    tmp2 = left_shift(y, 1);
    tmp2 = and(tmp2, left_shift(y, 8), N);
    tmp2 = xor(x, tmp2, N);
    tmp2 = xor(tmp2, left_shift(y, 2), N);
    x = copy_array(tmp, N);    
    y = xor(tmp2, keys[T - 1 - i], N);
  }

  return join_chunks(x, y, N, N);
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


int* and(int* arr1, int* arr2, int size) {
  int* tmp = malloc(sizeof(int) * size);
  
  for (int i = 0; i < size; i++) {    
    tmp[i] = arr1[i] & arr2[i];
  }

  return tmp;
}

int* left_shift(int* array, int times) {
  int i = 0, j = 0;
  int* tmp = malloc(sizeof(int) * N);
  tmp = copy_array(array, N);

  /* Shift to the left of an array */
  for (j = 0; j < times; j++) {
    int pos0 = tmp[0];
    for (i = 0; i < N - 1; i++) {
      tmp[i] = tmp[i + 1];
    }

    tmp[i] = pos0;
  }
  

  return tmp;
}

int* right_shift(int* array, int times) {
  int i = 0, j = 0;
  int* tmp = malloc(sizeof(int) * N);
  tmp = copy_array(array, N);

  /* Shift to the right of an array */
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

int* join_chunks(int* ch1, int* ch2, int s1, int s2) {
  int* join = malloc(sizeof(int) * (s1 + s2));
  
  for (int i = 0; i < s1; i++) {
    join[i] = ch1[i];
  }

  for (int i = s1, j = 0; i < (s1 + s2); i++, j++) {
    join[i] = ch2[j];
  }

  return join;
}

/* Function that prints an array on account of the size */
void print_array(int* array, int size) {
  for (int j = 0; j < size; j++) {
    printf("%d ", array[j]);
  }
  printf("\n");
}
