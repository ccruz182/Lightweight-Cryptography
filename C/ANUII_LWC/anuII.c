/*
  File name: present.c
  Author: Cesar Cruz
  Project: ANUII_LWC
*/
#include <stdio.h>
#include <stdlib.h>

/* 
	Constant's definition 
*/
#define KEY_SIZE 				128
#define ROUND_KEY_SIZE 	32
#define BLOCK_SIZE 			64
#define ROUNDS 					25

int SBOX[16] = {14, 4, 11, 1, 7, 9, 12, 10, 13, 2, 0, 15, 8, 5, 3, 6};


/* 
	Principal function's definition
*/
int** get_and_update_round_key(int* key, int round_counter);

/* 
	Auxiliar function's definition
*/
int 	array_to_int(int* array, int size);
int*	get_chunk(int* array, int begin, int final);
int* 	int_to_bin_array(int int_num, int size);
int* 	left_rotation(int* array, int times);
void 	print_array(int*array, int size);
int* 	replace_values(int* original, int* replacer, int begin, int end);
int* 	sbox_operation(int* state, int begin, int end, int num_bits);
int* 	xor(int* arr1, int* arr2, int size);

/* Main */
int main(void) {
	int key[KEY_SIZE], plaintext[BLOCK_SIZE];
  int i;
  int* state = malloc(sizeof(int) * BLOCK_SIZE);

  /* Key initialization */
  for (i = 0; i < KEY_SIZE; i++) {
    key[i] = 0;  
  }

  for (i = 0; i < ROUNDS; i++) {
  	printf("--> %d\n", i);
  	int** round_keys = get_and_update_round_key(key, i);  	
  	print_array(round_keys[0], ROUND_KEY_SIZE);
  	//print_array(round_keys[1], ROUND_KEY_SIZE);  	
	}
}


/* Function's implementation */
int** get_and_update_round_key(int* key, int round_counter) {  
  int* state = key;
  int** keys = (int **) malloc(sizeof(int) * 4);
  
  /* 
  	Extraction of the round key
  */

  // Key1 extraction
	int* key1 = malloc(sizeof(int) * 32);
	key1 = get_chunk(state, 96, KEY_SIZE); // K31 ... K0
	keys[0] = key1;

	// Key2 extraction
	int* key2 = malloc(sizeof(int) * 32);
	key2 = get_chunk(state, 64, 97); // K63 ... K32
	keys[1] = key2;
	
	/*
		Key update
	*/
	
	// Step 1. Rotate state to the left 13 times
	state = left_rotation(state, 13); // KEY <<< 13
	// printf("\t1. ");
	// print_array(state, KEY_SIZE);
	
	// Step 2. Substitution layer
	int* sbox_values = sbox_operation(state, 124, KEY_SIZE, 4); // KEY[3...0] = S(KEY[3...0])	
	state = replace_values(state, sbox_values, 124, KEY_SIZE);
	// printf("\t2. ");
	// print_array(state, KEY_SIZE);

	// Step 3. Substitution layer
	int* sbox_values2 = sbox_operation(state, 120, 124, 4); // KEY[7...4] = S(KEY[7...4])		
	state = replace_values(state, sbox_values2, 120, 124);
	// printf("\t3. ");
	// print_array(state, KEY_SIZE);	
	
	/* Step 4. X-OR with round counter */
	int* chunk_xor = get_chunk(state, 64, 69); 
	int* round_counter_bin = int_to_bin_array(round_counter, 5);    
	int* xor_result = xor(chunk_xor, round_counter_bin, 5);   
	state = replace_values(state, xor_result, 64, 69);
	// printf("\t4. ");
	// print_array(state, KEY_SIZE);
	 
	key = state;

  return keys;
}

/*
	Auxiliar function's implementation
*/

/* Function that converts an integer array (representing a binary) to a integer number */
int array_to_int(int* array, int size) {
  int value = 0;  
  
  for (int i = 0; i < size; i++) {    
    value += array[i] << (3 - i);    
  }

  return value;
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

/* Function that shift the content of an array to the left a number of positions (times) */
int* left_rotation(int* array, int times) {
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

/* Function that prints an array on account of the size */
void print_array(int* array, int size) {
  for (int j = 0; j < size; j++) {
    printf("%d ", array[j]);
  }
  printf("\n");
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

/* Function that makes a X-OR operation between two arrays (arr1, arr2) */
int* xor(int* arr1, int* arr2, int size) {
  for (int i = 0; i < size; i++) {    
    arr1[i] = arr1[i] != arr2[i];
  }

  return arr1;
}