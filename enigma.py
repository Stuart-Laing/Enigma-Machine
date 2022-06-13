
ALPH = "abcdefghijklmnopqrstuvwxyz"


class Scrambler:
    def __init__(self, output_config: str, input_config: str = ALPH):
        self.initial_input_config = input_config
        self.initial_output_config = output_config
        self.input_config = input_config
        self.output_config = output_config
        self.current_shift = 0

    def reset(self):
        self.input_config = self.initial_input_config
        self.output_config = self.initial_output_config
        self.current_shift = 0

    def tick(self, turns: int = 1) -> int:
        # Returns number of full turns completed

        full_turns = 0
        for i in range(0, turns):
            self.input_config = self.input_config[1:] + self.input_config[0]
            self.output_config = self.output_config[1:] + self.output_config[0]

            self.current_shift += 1
            if self.current_shift == 26:
                self.current_shift = 0
                full_turns += 1
        return full_turns

    def scramble_forward(self, index: int) -> int:
        return self.output_config.index(self.input_config[index])

    def scramble_backward(self, index: int) -> int:
        return self.input_config.index(self.output_config[index])


class Reflector:
    def __init__(self, config: str):
        self.config = config
        self.alph = ALPH

    def reflect(self, index: int) -> int:
        return self.config.index(self.alph[index])


class Plugboard:
    def __init__(self, swap_string_a: str, swap_string_b: str):
        self.swap_dict = {}
        for i, c in enumerate(swap_string_a):
            self.swap_dict[c] = swap_string_b[i]
            self.swap_dict[swap_string_b[i]] = c

    def swap(self, c: str):
        return self.swap_dict.get(c, c)


class Machine:
    def __init__(self, reflector: Reflector, plugboard: Plugboard,  *scramblers: Scrambler):
        self.reflector = reflector
        self.plugboard = plugboard
        self.scramblers = scramblers

    def compute(self, input_string: str) -> str:
        output_string = ""

        for c in input_string:
            self.send_tick()

            index = ALPH.index(self.plugboard.swap(c))
            for scrambler in self.scramblers:
                # print(f"scramble 1 {c}, {index}", end="")
                index = scrambler.scramble_forward(index)
                # print(f" -> {index}")
            # print(f"reflect {c}, {index}", end="")
            index = self.reflector.reflect(index)
            # print(f" -> {index}")

            for scrambler in reversed(self.scramblers):
                # print(f"scramble 2 {c}, {index}", end="")
                index = scrambler.scramble_backward(index)
                # print(f" -> {index}")
            # print()
            output_string += self.plugboard.swap(ALPH[index])

        return output_string

    def send_tick(self):
        turns_for_next_scrambler = 1
        for scrambler in self.scramblers:
            turns_for_next_scrambler = scrambler.tick(turns_for_next_scrambler)

    def reset(self):
        for scrambler in self.scramblers:
            scrambler.reset()
