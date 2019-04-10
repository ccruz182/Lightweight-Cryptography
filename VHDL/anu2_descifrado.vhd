LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity anu2 is
  Port (  key :       in  STD_LOGIC_VECTOR (127 downto 0);
          ciphertext: in  STD_LOGIC_VECTOR (63 downto 0);
          clk:        in  STD_LOGIC;
          clr:        in  STD_LOGIC;
          key_out:    out STD_LOGIC_VECTOR (127 downto 0);
          plaintext:  out STD_LOGIC_VECTOR (63 downto 0));
end anu2;

architecture Descifrado of anu2 is
-- Definicion de tipo memoria para sbox.
TYPE mem IS ARRAY (0 TO 15) OF STD_LOGIC_VECTOR(3 DOWNTO 0);
TYPE mem2 IS ARRAY (0 TO 24) OF STD_LOGIC_VECTOR(63 DOWNTO 0);

-- Declaracion de la sbox, que es una memoria.
CONSTANT sbox: mem := (
	x"E", x"4", x"B", x"1",
	x"7", x"9", x"C", x"A",
	x"D", x"2", x"0", x"F",
	x"8", x"5", x"3", x"6"
);

CONSTANT sbox_inv: mem := (
	x"A", x"3", x"9", x"E",
	x"1", x"D", x"F", x"4",
	x"C", x"5", x"7", x"2",
	x"6", x"8", x"0", x"B"
);

begin 
	process (clk, clr, ciphertext, key)
		-- Declaracion de las variables a ocupar.
		variable input_bits:    STD_LOGIC_VECTOR (63 DOWNTO 0);
		variable a_unsig:       UNSIGNED (127 DOWNTO 0);
		variable b_unsig:       UNSIGNED (31 DOWNTO 0);
		variable key_round:     STD_LOGIC_VECTOR (63 DOWNTO 0);
		variable round_counter: STD_LOGIC_VECTOR (4 DOWNTO 0);
		variable temp1:         STD_LOGIC_VECTOR (31 DOWNTO 0);
		variable sbox_index:    STD_LOGIC_VECTOR (3 DOWNTO 0);
		variable master_key:    STD_LOGIC_VECTOR (127 downto 0);
		
		variable round_keys:		mem2;
		
		begin
      input_bits := ciphertext(63 DOWNTO 0);
      master_key := key(127 downto 0);
      
		-- Generacion de subllaves
      for I in 0 to 24 loop
        if (clr = '1') then
          plaintext <= (others => '1');			
        elsif(rising_edge(clk))then                    
          -- Extraccion de las llaves
          round_keys(I) := master_key(63 DOWNTO 0);
                  
          -- Rotacion
          a_unsig := UNSIGNED(master_key);
          master_key := STD_LOGIC_VECTOR(a_unsig ROL 13);
                  
          -- Operaciones con SBOX
          sbox_index := master_key(3 DOWNTO 0);
          master_key(3 DOWNTO 0) := 
              sbox(to_integer(unsigned(sbox_index)));
                  
          sbox_index := master_key(7 DOWNTO 4);
          master_key(7 DOWNTO 4) := 
              sbox(to_integer(unsigned(sbox_index)));
                  
          -- Operacion XOR con contador I
          round_counter := std_logic_vector(to_unsigned(I, 5));		
          master_key(63 DOWNTO 59) := 
              master_key(63 DOWNTO 59) XOR round_counter;
			end if;
		end loop;
						
		-- Descifrado
		for I in 0 to 24 loop
        if (clr = '1') then
          plaintext <= (others => '1');			
        elsif(rising_edge(clk))then
          -- Swap
          temp1 := input_bits(63 DOWNTO 32);
          input_bits(63 DOWNTO 32) := input_bits(31 DOWNTO 0);
          input_bits(31 DOWNTO 0) := temp1;
			 			 			
          -- Rotacion
          b_unsig := UNSIGNED(input_bits(63 DOWNTO 32));
          temp1 := STD_LOGIC_VECTOR(b_unsig ROL 10);			 		
			 
          -- AddRoundKey2:
          input_bits(31 DOWNTO 0) := 
              input_bits(31 DOWNTO 0) XOR temp1 
                XOR round_keys(24 - I)(63 DOWNTO 32);					 		
					 
          -- Rotacion					
          b_unsig := UNSIGNED(input_bits(31 DOWNTO 0));
          temp1 := STD_LOGIC_VECTOR(b_unsig ROR 3);

          -- AddRoundKey1
          input_bits(63 DOWNTO 32) := 
              input_bits(63 DOWNTO 32) XOR temp1 
                XOR round_keys(24 - I)(31 DOWNTO 0);		

          for J in 0 to 7 loop						
            sbox_index := input_bits((63 - 4*J) DOWNTO (60 - 4*J));						
            input_bits((63 - 4*J) DOWNTO (60 - 4*J)) := 
                sbox_inv(to_integer(unsigned(sbox_index)));
          end loop;
 			 plaintext <= input_bits;
			 key_out(63 DOWNTO 0) <= round_keys(24 - I);
		  end if;
		end loop;				
	end process;
end Descifrado;

