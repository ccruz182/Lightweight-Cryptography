#include <stdio.h>
#include <stdlib.h>

#define KEY_LENGHT 80
int SBOX[16] = {12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2};

int** generate_round_keys(int* key);

/* Auxiliar functions */
int* left_shift(int* array, int times);
void print_array(int*array, int size);
int* get_chunk(int* array, int begin, int final);
int array_to_int(int* array, int size);
int* int_to_bin_array(int int_num, int size);
int* replace_values(int* original, int* replacer, int begin, int end);
int* xor(int* arr1, int* arr2, int size);

int main(void) {
	int key[KEY_LENGHT];

  for (int i = 0; i < 80; i++) {
    key[i] = 0;
  }

	int** keys = generate_round_keys(key);
    
	return 0;
}


int** generate_round_keys(int* key) {  
  int round_counter;
  int* state = key;
  int** keys = (int **) malloc(sizeof(int) * 4);

  for (round_counter = 1; round_counter < 33; round_counter++) {
    int* new_key = malloc(sizeof(int) * 64);
    new_key = get_chunk(state, 0, 64);
    keys[round_counter - 1] = new_key;
    
    printf("Round %d\n", round_counter);
    // printf("\tState.\t");
    // print_array(state, 80);

    /* Step 1. Rotate state to the left 61 times */
    state = left_shift(state, 61); 
    // printf("\tStep 1.\t");
    // print_array(state, 80);   

    /* Step 2. Substitution layer */
    int* chunk = get_chunk(state, 0, 4);
    int sbox_index = array_to_int(chunk, 4);
    int* sbox_values = int_to_bin_array(SBOX[sbox_index], 4);
    state = replace_values(state, sbox_values, 0, 4);
    // printf("\tStep 2.\t");
    // print_array(state, 80);

    /* Step 3. X-OR with round counter */
    int* chunk_xor = get_chunk(state, 60, 65); 
    int* round_counter_bin = int_to_bin_array(round_counter, 5);    
    int* xor_result = xor(chunk_xor, round_counter_bin, 5);   
    state = replace_values(state, xor_result, 60, 65);

    // printf("\tStep 3.\t");
    // print_array(state, 80);

    printf("KEY: ");
    print_array(new_key, 32);
    printf("------------------\n");
  }

  for (int k = 0; k < 32; k++) {
    printf("Key %d: ", k);
    print_array(keys[k], 64);
  }

  return keys;
}

int* left_shift(int* array, int times) {
  int i = 0, j = 0;

  for (j = 0; j < times; j++) {
    int pos0 = array[0];
    for (i = 0; i < KEY_LENGHT - 1; i++) {
      array[i] = array[i + 1];
    }

    array[i] = pos0;
  }
  

  return array;
}

int* get_chunk(int* array, int begin, int final) {  
  int size = final - begin;
  int* chunk = malloc(sizeof(int) * size);

  for (int i = begin, j = 0; i < final; i++, j++) {
    chunk[j] = array[i];    
  }  

  return chunk;
}

void print_array(int* array, int size) {
  for (int j = 0; j < size; j++) {
    printf("%d ", array[j]);
  }
  printf("\n");
}

int array_to_int(int* array, int size) {
  int valor = 0;  
  
  for (int i = 0; i < size; i++) {    
    valor += array[i] << (3 - i);    
  }

  return valor;
}

int* int_to_bin_array(int int_num, int size) {
  int* bin_array = malloc(sizeof(int) * size);
  int div = int_num;
  int i = size - 1;

  while (div != 0) {
    bin_array[i] = div % 2;
    div /= 2;
    i--;
  }

  return bin_array;
}

int* replace_values(int* original, int* replacer, int begin, int end) {
  int diff = end - begin;

  for (int i = 0, j = begin; i < diff; i++, j++) {
    original[j] = replacer[i];
  }

  return original;
}

int* xor(int* arr1, int* arr2, int size) {
  for (int i = 0; i < size; i++) {    
    arr1[i] = arr1[i] != arr2[i];
  }

  return arr1;
}