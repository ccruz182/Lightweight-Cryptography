library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
USE ieee.numeric_std.ALL;

entity anu2 is
    Port ( key : in  STD_LOGIC_VECTOR (127 downto 0);
				plaintext: in STD_LOGIC_VECTOR (63 downto 0);
				clk: in STD_LOGIC;
				clr: in 	STD_LOGIC;
				key_out: out std_logic_vector(127 downto 0);
           ciphertext : out  STD_LOGIC_VECTOR (63 downto 0));
end anu2;

architecture Behavioral of anu2 is
-- Definicion de tipo memoria para sbox 
TYPE mem IS ARRAY (0 TO 15) OF STD_LOGIC_VECTOR(3 DOWNTO 0);
SIGNAL sbox: mem;

begin 
	-- Definicion de SBOX --
	sbox(0) <= x"E"; sbox(1) <= x"4"; sbox(2) <= x"B"; sbox(3) <= x"1";
	sbox(4) <= x"7"; sbox(5) <= x"9"; sbox(6) <= x"C"; sbox(7) <= x"A";
	sbox(8) <= x"D"; sbox(9) <= x"2"; sbox(10) <= x"0"; sbox(11) <= x"F";
	sbox(12) <= x"8"; sbox(13) <= x"5"; sbox(14) <= x"3"; sbox(15) <= x"6";
	
	process (clk, clr, sbox, plaintext, key)
		variable input_bits: STD_LOGIC_VECTOR (63 DOWNTO 0);
		variable	a_unsig: UNSIGNED(127 DOWNTO 0);
		variable	b_unsig: UNSIGNED(31 DOWNTO 0);
		variable key_round: STD_LOGIC_VECTOR(63 DOWNTO 0);
		variable round_counter: STD_LOGIC_VECTOR(4 DOWNTO 0);
		variable temp1: STD_LOGIC_VECTOR (31 DOWNTO 0);
		variable sbox_index: STD_LOGIC_VECTOR(3 DOWNTO 0);
		variable master_key: std_logic_vector(127 downto 0);
		
		begin
			if (clr = '1') then
				ciphertext <= (others => '0');			
			elsif(rising_edge(clk))then
				input_bits := plaintext(63 DOWNTO 0);
				master_key := key(127 downto 0);
				
				for I in 0 to 24 loop
					key_out <= master_key;
					-- Extraccion de las llaves
					key_round := master_key(63 DOWNTO 0);
									
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
			
					--A) Apply S-Box to input_bits(63 downto 32)
					--TEMP) Save state of input_bits(31 downto 0) to TEMP1
					--B) Apply 3 postions right rotation to input_bits(31 downto 0)
					--C) Apply bitwise xor operation between A and B and Keyround1, it is saved at input_bits(63 downto 32)
					--TEMP2) Save state of input_bits(31 downto 0) to TEMP2
					--D) Apply 10 positions left rotation to C
					--E) Apply bitwise operation between B and TEMP and Keyround2
					--F) Swap positions between input_bits(31 downto 0) to input_bits(63 downto 32) and TEMP2 to input_bits(31 to 0)
					
					
					for J in 0 to 7 loop						
						sbox_index := input_bits((63 - 4*J) DOWNTO (60 - 4*J));						
						input_bits((63 - 4*J) DOWNTO (60 - 4*J)) := sbox(to_integer(unsigned(sbox_index)));
					end loop;
								
					-- Rotacion					
					b_unsig := UNSIGNED(input_bits(31 DOWNTO 0));
					temp1 := STD_LOGIC_VECTOR(b_unsig ROR 3);
										
					
					-- AddRoundKey1
					input_bits(63 DOWNTO 32) := input_bits(63 DOWNTO 32) XOR temp1 XOR key_round(31 DOWNTO 0);
					
					-- Rotacion
					b_unsig := UNSIGNED(input_bits(63 DOWNTO 32));
					temp1 := STD_LOGIC_VECTOR(b_unsig ROL 10);
					
					-- AddRoundKey2:
					input_bits(31 DOWNTO 0) := input_bits(31 DOWNTO 0) XOR temp1 XOR key_round(63 DOWNTO 32);
					
					
					-- Swap
					temp1 := input_bits(63 DOWNTO 32);
					input_bits(63 DOWNTO 32) := input_bits(31 DOWNTO 0);
					input_bits(31 DOWNTO 0) := temp1;
			end loop;
			end if;
			ciphertext <= input_bits;
	end process;
end Behavioral;

