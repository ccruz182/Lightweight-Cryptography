/*
  File name: present.c
  Author: Cesar Cruz
  Project: Present_LWC
*/

#include <stdio.h>
#include <stdlib.h>

#define KEY_SIZE 80
#define BLOCK_SIZE 64
int SBOX[16] = {12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2};

/* Principal functions used in the cipher algorithm */
int** generate_round_keys(int* key);
int* add_round_key(int* state, int* key);
int* sbox_layer(int* state);
int* pbox_layer(int* state, int* pbox);

/* Auxiliar functions */
int* left_shift(int* array, int times);
void print_array(int*array, int size);
int* get_chunk(int* array, int begin, int final);
int array_to_int(int* array, int size);
int* int_to_bin_array(int int_num, int size);
int* replace_values(int* original, int* replacer, int begin, int end);
int* xor(int* arr1, int* arr2, int size);
int* generate_pbox();
int* sbox_operation(int* state, int begin, int end, int num_bits);

int main(void) {
	int key[KEY_SIZE], plaintext[BLOCK_SIZE];
  int i;

  int* state = malloc(sizeof(int) * BLOCK_SIZE);

  for (i = 0; i < KEY_SIZE; i++) {
    key[i] = 0;  
  }

  for (i = 0; i < BLOCK_SIZE; i++) {
    plaintext[i] = 0;  
    state[i] = 0;
  }

  /* Present. Cryptographic algorithm */
	int** keys = generate_round_keys(key);
  
  int* pbox = generate_pbox();

  /* Rounds of the algorithm */
  for (i = 0; i < 31; i++) {
    // printf("Round %d\n", i);

    /* Step 1. Add round key */
    state = add_round_key(state, keys[i]);
    // printf("add_round_key: ");
    // print_array(state, BLOCK_SIZE);

    /* Step 2. Sbox layer */
    state = sbox_layer(state);
    // printf("sbox_layer: ");
    // print_array(state, BLOCK_SIZE);

    /* Step 3. Pbox layer */
    state = pbox_layer(state, pbox);
    // printf("sbox_layer: ");
    // print_array(state, BLOCK_SIZE);
  }

  state = add_round_key(state, keys[i]);

  printf("Final: ");
  print_array(state, BLOCK_SIZE);

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
    
    // printf("Round %d\n", round_counter);
    // printf("\tState.\t");
    // print_array(state, 80);

    /* Step 1. Rotate state to the left 61 times */
    state = left_shift(state, 61); 
    // printf("\tStep 1.\t");
    // print_array(state, 80);   

    /* Step 2. Substitution layer */
    int* sbox_values = sbox_operation(state, 0, 4, 4);
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
  }

/*
  for (int k = 0; k < 32; k++) {
    printf("Key %d: ", k);
    print_array(keys[k], 64);
  }
*/

  return keys;
}

/* add_round_key operation */
int* add_round_key(int* state, int* key) {
  int* new_state = malloc(sizeof(int) * BLOCK_SIZE);

  new_state = xor(state, key, BLOCK_SIZE);

  return new_state;
}

/* sbox_layer operation */
int* sbox_layer(int* state) {
  int i, begin;

  for (i = 0; i < (BLOCK_SIZE / 4); i++) {
    begin = 4 * i;
    int* sbox_values = sbox_operation(state, begin, begin + 4, 4);
    state = replace_values(state, sbox_values, begin, begin + 4);
  }

  return state;
}

/* pbox_layer operation */
int* pbox_layer(int* state, int* pbox) {
  int* new_state = malloc(sizeof(int) * BLOCK_SIZE);
  int i;

  for (i = 0; i < BLOCK_SIZE; i++) {
    new_state[pbox[i]] = state[i];
  }

  return new_state;
}

/** 
  Auxiliar functions 
  **/

/* Function that shift the content of an array to the left a number of positions (times) */
int* left_shift(int* array, int times) {
  int i = 0, j = 0;

  /* Shift to the left of an array */
  for (j = 0; j < times; j++) {
    int pos0 = array[0];
    for (i = 0; i < KEY_SIZE - 1; i++) {
      array[i] = array[i + 1];
    }

    array[i] = pos0;
  }
  

  return array;
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

/* Function that converts an integer array (representing a binary) to a integer number */
int array_to_int(int* array, int size) {
  int value = 0;  
  
  for (int i = 0; i < size; i++) {    
    value += array[i] << (3 - i);    
  }

  return value;
}

/* Function that converts an integer number to a integer array (representing a binary) of a 
    specified size */
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

/* Function that replaces a chunk (replacer) in a specified position (begin, end) on an 
    original array (original) */
int* replace_values(int* original, int* replacer, int begin, int end) {
  int diff = end - begin;

  for (int i = 0, j = begin; i < diff; i++, j++) {
    original[j] = replacer[i];
  }

  return original;
}

/* Function that makes a X-OR operation between two arrays (arr1, arr2) */
int* xor(int* arr1, int* arr2, int size) {
  for (int i = 0; i < size; i++) {    
    arr1[i] = arr1[i] != arr2[i];
  }

  return arr1;
}

/* Function that generates the PBOX used in the Present Algorithm */
int* generate_pbox() {
  int i, j;
  int* pbox = malloc(sizeof(int) * 64);

  for (i = 0; i < 16; i++) {
    for (j = 0; j < 4; j++) {
      pbox[(i * 4) + j] = i + (16 * j);
    }
  }

  return pbox;
}

/* Function that returns the SBOX values of a chunk */
int* sbox_operation(int* state, int begin, int end, int num_bits) {
  /* First, get the chunk of state */
  int* chunk = get_chunk(state, begin, end);

  /* Then, convert that chunk in an integer */
  int sbox_index = array_to_int(chunk, num_bits);

  /* Finally, convert into an array of bits (actually, integers representing
     a binary string. */
  int* sbox_values = int_to_bin_array(SBOX[sbox_index], num_bits);

  return sbox_values;
}