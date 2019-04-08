library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
USE ieee.numeric_std.ALL;

entity anu is
    Port ( 	key : 		in		STD_LOGIC_VECTOR(127 downto 0);
				plaintext: 	in 	STD_LOGIC_VECTOR(63 downto 0);
				clk: 			in 	STD_LOGIC;
				clr: 			in 	STD_LOGIC;
				key_out: 	out	STD_LOGIC_VECTOR(127 downto 0);
				ciphertext: out  	STD_LOGIC_VECTOR (63 downto 0));
end anu;

architecture Behavioral of anu is
-- Definicion de tipo memoria para sbox 
TYPE mem IS ARRAY (0 TO 15) OF STD_LOGIC_VECTOR(3 DOWNTO 0);
SIGNAL sbox: mem;

TYPE mem2 IS ARRAY (0 TO 31) OF INTEGER RANGE 0 TO 31;
SIGNAL pbox: mem2;

begin 
	-- Definicion de SBOX --
	sbox(0) <= x"2"; sbox(1) <= x"9"; sbox(2) <= x"7"; sbox(3) <= x"E";
	sbox(4) <= x"1"; sbox(5) <= x"C"; sbox(6) <= x"A"; sbox(7) <= x"0";
	sbox(8) <= x"4"; sbox(9) <= x"3"; sbox(10) <= x"8"; sbox(11) <= x"D";
	sbox(12) <= x"F"; sbox(13) <= x"6"; sbox(14) <= x"5"; sbox(15) <= x"B";
	
	-- Permutation Box Definition --
	pbox(0) <= 20; pbox(1) <= 16; pbox(2) <= 28; pbox(3) <= 24; pbox(4) <= 17; pbox(5) <= 21; pbox(6) <= 25; pbox(7) <= 29;
	pbox(8) <= 22; pbox(9) <= 18; pbox(10) <= 30; pbox(11) <= 26; pbox(12) <= 19; pbox(13) <= 23; pbox(14) <= 27; pbox(15) <= 31;
	pbox(16) <= 11; pbox(17) <= 15; pbox(18) <= 3; pbox(19) <= 7; pbox(20) <= 14; pbox(21) <= 10; pbox(22) <= 6; pbox(23) <= 2;
	pbox(24) <= 9; pbox(25) <= 13; pbox(26) <= 1; pbox(27) <= 5; pbox(28) <= 12; pbox(29) <= 8; pbox(30) <= 4; pbox(31) <= 0;
	
	process (clk, clr, sbox, plaintext, key)
		variable input_bits: 	STD_LOGIC_VECTOR (63 DOWNTO 0);
		
		variable	a_unsig: 		UNSIGNED(127 DOWNTO 0);
		variable	b_unsig: 		UNSIGNED(31 DOWNTO 0);
		
		variable key_round: 		STD_LOGIC_VECTOR(31 DOWNTO 0);
		variable master_key: 	STD_LOGIC_VECTOR(127 downto 0);
		
		variable f1: 				STD_LOGIC_VECTOR(31 DOWNTO 0);
		variable f2: 				STD_LOGIC_VECTOR(31 DOWNTO 0);
		
		variable sbox_index: 	STD_LOGIC_VECTOR(3 DOWNTO 0);
		variable round_counter: STD_LOGIC_VECTOR(4 DOWNTO 0);
		
		begin
			if (clr = '1') then
				ciphertext <= (others => '0');			
			elsif(rising_edge(clk))then
				input_bits := plaintext(63 DOWNTO 0);
				master_key := key(127 downto 0);
				
				for I in 0 to 24 loop
					key_out <= master_key;
					-- Extraccion de las llaves
					key_round := master_key(31 DOWNTO 0);
									
					-- Rotacion
					a_unsig := UNSIGNED(master_key);
					master_key := STD_LOGIC_VECTOR(a_unsig ROL 13);
									
					-- Operaciones con SBOX
					sbox_index := master_key(3 DOWNTO 0);
					master_key(3 DOWNTO 0) := sbox(to_integer(unsigned(sbox_index)));
									
					sbox_index := master_key(7 DOWNTO 4);
					master_key(7 DOWNTO 4) := sbox(to_integer(unsigned(sbox_index)));
									
					-- Operacion XOR con contador I
					round_counter := std_logic_vector(to_unsigned(I, 5));		
					master_key(63 DOWNTO 59) := master_key(63 DOWNTO 59) XOR round_counter;	
			
					------------------------------------------------------------------------------------
					------------------------------------- CIPHER ---------------------------------------
					------------------------------------------------------------------------------------
					
					-- First, F function
					-- 1. Get F1
					
					--  1.1 Left rotation by 3 bits of input_bits(63 DOWNTO 32)
					b_unsig := UNSIGNED(input_bits(63 DOWNTO 32));
					f1 := STD_LOGIC_VECTOR(b_unsig ROL 3);
					
					--  1.2 Sbox of 1.1
					for J in 0 to 7 loop
						sbox_index := f1((31 - 4*J) DOWNTO (28 - 4*J));
						f1((31 - 4*J) DOWNTO (28 - 4*J)) := sbox(to_integer(unsigned(sbox_index)));
					end loop;
					
					--  1.3 XOR between f1 and input_bits(31 DOWNTO 0)
					f1 := f1 xor input_bits(31 DOWNTO 0);
					
					-- 2. Get G2
					
					--  2.1 Right rotation by 8 bits of input(63 DOWNTO 32)
					b_unsig := UNSIGNED(input_bits(63 DOWNTO 32));
					f2 := STD_LOGIC_VECTOR(b_unsig ROR 8);
					
					--  2.2 Sbox of 2.1
					for J in 0 to 7 loop
						sbox_index := f2((31 - 4*J) DOWNTO (28 - 4*J));
						f2((31 - 4*J) DOWNTO (28 - 4*J)) := sbox(to_integer(unsigned(sbox_index)));
					end loop;
					
					--  2.3 XOR between f1 (1.3), f2 and key_round
					f2 := f1 xor f2 xor key_round;
					
					-- 3. Permutation
					
					--  3.1 Permutation of input_bits(63 DOWNTO 32)
					for J in 0 to 31 loop
						f1(pbox(J)) := input_bits(J + 32);
					end loop;
					
					-- 3.2 Permutation of f2
					for J in 0 to 31 loop
						input_bits(pbox(J)) := f2(J);
					end loop;
					
					
					-- Swap					
					input_bits(63 DOWNTO 32) := input_bits(31 DOWNTO 0);
					input_bits(31 DOWNTO 0) := f1;
				end loop;				
			end if;
			ciphertext <= input_bits;
	end process;
end Behavioral;

