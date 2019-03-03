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
int* sbox_layer(int* state);


/* 
	Auxiliar function's definition
*/
int 	array_to_int(int* array, int size);
int* 	copy_array(int* origin, int size);
int*	get_chunk(int* array, int begin, int final);
int* 	int_to_bin_array(int int_num, int size);
int* 	left_rotation(int* array, int times, int array_size);
void 	print_array(int*array, int size);
int* 	replace_values(int* original, int* replacer, int begin, int end);
int* 	right_rotation(int* array, int times, int array_size);
int* 	sbox_operation(int* state, int begin, int end, int num_bits);
int* 	xor(int* arr1, int* arr2, int size);

/* Main */
int main(void) {
	int* key = malloc(sizeof(int) * KEY_SIZE);
  int i;
  int* left = malloc(sizeof(int) * BLOCK_SIZE / 2);
  int* right = malloc(sizeof(int) * BLOCK_SIZE / 2);

  /* init vector */
  for (i = 0; i < BLOCK_SIZE; i++) {    
    if (i < BLOCK_SIZE / 2) {
    	left[i] = 0;
    } else {
    	right[BLOCK_SIZE / 2 - i] = 0;
    }
  }

  /* Key initialization */
  for (i = 0; i < KEY_SIZE; i++) {
    key[i] = 0;  
  }

  for (i = 0; i < ROUNDS; i++) {
  	// printf("--> %d\n", i);

  	/* First, the round keys are generated */  	
  	int** round_keys = get_and_update_round_key(key, i);  	
  	key = copy_array(round_keys[2], KEY_SIZE);  
  	
  	/* SBOX with the left side of the state */
  	left = sbox_layer(get_chunk(left, 0, 32)); // SBOX[P_MSB]
  	// print_array(left, ROUND_KEY_SIZE);
  	
  	/* Right rotation by 3 bits */
  	int* tmp_right = right_rotation(right, 3, ROUND_KEY_SIZE);
  	// print_array(tmp_right, ROUND_KEY_SIZE);

		/* XOR with RK1 */
		left = xor(left, xor(tmp_right, round_keys[0], ROUND_KEY_SIZE), ROUND_KEY_SIZE);
  	// print_array(left, ROUND_KEY_SIZE);

		/* Left rotation by 10 bits */
		int* tmp_left = left_rotation(left, 10, ROUND_KEY_SIZE);
		// print_array(tmp_left, ROUND_KEY_SIZE);

		/* XOR with RK2 */
		tmp_left = xor(right, xor(tmp_left, round_keys[1], ROUND_KEY_SIZE), ROUND_KEY_SIZE);
		// print_array(tmp_left, ROUND_KEY_SIZE);

		right = copy_array(left, ROUND_KEY_SIZE);
		left = copy_array(tmp_left, ROUND_KEY_SIZE);
	}

	printf("LEFT: ");
	print_array(left, ROUND_KEY_SIZE);
	printf("RIGHT: ");
	print_array(right, ROUND_KEY_SIZE);
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
	state = left_rotation(state, 13, KEY_SIZE); // KEY <<< 13
		
	// Step 2. Substitution layer
	int* sbox_values = sbox_operation(state, 124, KEY_SIZE, 4); // KEY[3...0] = S(KEY[3...0])	
	state = replace_values(state, sbox_values, 124, KEY_SIZE);

	// Step 3. Substitution layer
	int* sbox_values2 = sbox_operation(state, 120, 124, 4); // KEY[7...4] = S(KEY[7...4])		
	state = replace_values(state, sbox_values2, 120, 124);
	
	/* Step 4. X-OR with round counter */
	int* chunk_xor = get_chunk(state, 64, 69); 
	int* round_counter_bin = int_to_bin_array(round_counter, 5);    
	int* xor_result = xor(chunk_xor, round_counter_bin, 5);   
	state = replace_values(state, xor_result, 64, 69);
	 
	key = copy_array(state, KEY_SIZE);
	keys[2] = copy_array(state, KEY_SIZE);

  return keys;
}

/* sbox_layer operation */
int* sbox_layer(int* state) {
  int i, begin;

  for (i = 0; i < (BLOCK_SIZE / 8); i++) {
    begin = 4 * i;
    int* sbox_values = sbox_operation(state, begin, begin + 4, 4);
    state = replace_values(state, sbox_values, begin, begin + 4);
  }

  return state;
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
int* left_rotation(int* array, int times, int array_size) {
  int i = 0, j = 0;
  int* tmp = malloc(sizeof(int) * array_size);
  tmp = copy_array(array, array_size);

  /* Shift to the left of an array */
  for (j = 0; j < times; j++) {
    int pos0 = tmp[0];
    for (i = 0; i < array_size - 1; i++) {
      tmp[i] = tmp[i + 1];
    }

    tmp[i] = pos0;
  }
  
  return tmp;
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

int* right_rotation(int* array, int times, int array_size) {
  int i = 0, j = 0;
  int* tmp = malloc(sizeof(int) * array_size);
  tmp = copy_array(array, array_size);

  /* Shift to the right of an array */
  for (j = 0; j < times; j++) {
    int posN = tmp[array_size - 1];
    
    for (i = array_size - 1; i > 0; i--) {
      tmp[i] = tmp[i - 1];
    }

    tmp[0] = posN;
  }
  
  return tmp;
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