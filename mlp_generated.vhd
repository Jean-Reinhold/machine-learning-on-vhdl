-- Auto-generated VHDL MLP
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity MLP is
    Port (
        input_vec  : in  INTEGER_VECTOR(1 downto 0);
        output_bit : out STD_LOGIC
    );
end MLP;

architecture Behavioral of MLP is
    constant weights_layer_0 : array(0 to 1, 0 to 1) of integer := (
        (1, -2),
        (3, 4)
    );

    constant biases_layer_0 : INTEGER_VECTOR(1 downto 0) := (1, -1);

    constant weights_layer_1 : array(0 to 1, 0 to 0) of integer := (
        (2),
        (-1)
    );

    constant biases_layer_1 : INTEGER_VECTOR(0 downto 0) := (0);

begin
    process(input_vec)
        variable sum_val : integer;
        variable layer_0_output : INTEGER_VECTOR(1 downto 0);
        variable layer_1_output : INTEGER_VECTOR(0 downto 0);
    begin

        for j in 0 to 1 loop
            layer_0_output(j) := biases_layer_0(j);
            for k in 0 to 1 loop
                layer_0_output(j) := layer_0_output(j) + (input_vec(k) * weights_layer_0(k, j));
            end loop;
        end loop;

        for j in 0 to 0 loop
            layer_1_output(j) := biases_layer_1(j);
            for k in 0 to 1 loop
                layer_1_output(j) := layer_1_output(j) + (layer_0_output(k) * weights_layer_1(k, j));
            end loop;
        end loop;

        if layer_1_output(0) > 0 then
            output_bit <= '1';
        else
            output_bit <= '0';
        end if;

    end process;
end Behavioral;
