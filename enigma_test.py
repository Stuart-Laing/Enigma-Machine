import unittest
from enigma import *
ALPH = "abcdefghijklmnopqrstuvwxyz"


class TestScrambler(unittest.TestCase):
    def test_scramble_forward(self):
        s = Scrambler("uwygadfpvzbeckmthxslrinqoj")
        self.assertEqual(7, s.scramble_forward(15))

        self.assertEqual(4, s.scramble_forward(0))

        self.assertEqual(9, s.scramble_forward(25))

    def test_scramble_backward(self):
        s = Scrambler("uwygadfpvzbeckmthxslrinqoj")
        self.assertEqual(15, s.scramble_backward(7))

        self.assertEqual(0, s.scramble_backward(4))

        self.assertEqual(25, s.scramble_backward(9))

    def test_tick_scramble(self):
        s = Scrambler("uwygadfpvzbeckmthxslrinqoj")

        self.assertEqual(ALPH, s.input_config)
        self.assertEqual("uwygadfpvzbeckmthxslrinqoj", s.output_config)
        self.assertEqual(7, s.scramble_forward(15))

        self.assertFalse(s.tick())
        self.assertEqual("bcdefghijklmnopqrstuvwxyza", s.input_config)
        self.assertEqual("wygadfpvzbeckmthxslrinqoju", s.output_config)
        self.assertEqual(22, s.scramble_forward(15))

        self.assertFalse(s.tick())
        self.assertEqual("cdefghijklmnopqrstuvwxyzab", s.input_config)
        self.assertEqual("ygadfpvzbeckmthxslrinqojuw", s.output_config)
        self.assertEqual(18, s.scramble_forward(15))

    def test_tick_full_rotate(self):
        s = Scrambler("uwygadfpvzbeckmthxslrinqoj")

        self.assertEqual(0, s.tick(25))
        self.assertEqual(1, s.tick())

        self.assertEqual(ALPH, s.input_config)
        self.assertEqual("uwygadfpvzbeckmthxslrinqoj", s.output_config)
        self.assertEqual(7, s.scramble_forward(15))

    def test_reset(self):
        s = Scrambler("uwygadfpvzbeckmthxslrinqoj")

        self.assertEqual(7, s.scramble_forward(15))
        s.tick()
        s.tick()
        s.reset()
        self.assertEqual(ALPH, s.input_config)
        self.assertEqual("uwygadfpvzbeckmthxslrinqoj", s.output_config)
        self.assertEqual(7, s.scramble_forward(15))


class TestReflector(unittest.TestCase):
    def test_reflect(self):
        r = Reflector("yruhqsldpxngokmiebfzcwvjat")
        self.assertEqual(11, r.reflect(6))
        self.assertEqual(24, r.reflect(0))
        self.assertEqual(19, r.reflect(25))


class TestPlugboard(unittest.TestCase):
    def test_swap(self):
        p = Plugboard("asugle", "bzyhqn")

        self.assertEqual("a", p.swap("b"))
        self.assertEqual("b", p.swap("a"))
        self.assertEqual("g", p.swap("h"))
        self.assertEqual("n", p.swap("e"))
        self.assertEqual("k", p.swap("k"))
        self.assertEqual("v", p.swap("v"))


class TestMachine(unittest.TestCase):
    def test_reset(self):
        s1 = Scrambler("crukezvgdsitqjnohwlafxpmby")
        s2 = Scrambler("nuqmrgawxtfposkcybjiehlzdv")
        s3 = Scrambler("ciqwvlnytgehdkpaxsfrbjmouz")
        r = Reflector("yruhqsldpxngokmiebfzcwvjat")
        p = Plugboard("", "")
        m = Machine(r, p, s1, s2, s3)

        m.scramblers[0].tick()
        m.scramblers[1].tick()
        m.scramblers[2].tick()

        m.reset()

        self.assertEqual(ALPH, m.scramblers[0].input_config)
        self.assertEqual("crukezvgdsitqjnohwlafxpmby", m.scramblers[0].output_config)

        self.assertEqual(ALPH, m.scramblers[1].input_config)
        self.assertEqual("nuqmrgawxtfposkcybjiehlzdv", m.scramblers[1].output_config)

        self.assertEqual(ALPH, m.scramblers[2].input_config)
        self.assertEqual("ciqwvlnytgehdkpaxsfrbjmouz", m.scramblers[2].output_config)

    def test_compute_one_scrambler(self):
        s = Scrambler("uwygadfpvzbeckmthxslrinqoj")
        r = Reflector("yruhqsldpxngokmiebfzcwvjat")
        p = Plugboard("", "")
        m = Machine(r, p, s)

        self.assertEqual("zydni", m.compute("ultra"))
        m.reset()
        self.assertEqual("ultra", m.compute("zydni"))

    def test_compute_two_scramblers(self):
        s1 = Scrambler("uwygadfpvzbeckmthxslrinqoj")
        s2 = Scrambler("joqnirlsxhtmkcebzvpfdagywu", "zyxwvutsrqponmlkjihgfedcba")
        r = Reflector("yruhqsldpxngokmiebfzcwvjat")
        p = Plugboard("", "")
        m = Machine(r, p, s1, s2)

        self.assertEqual("hlcqpw", m.compute("enigma"))
        m.reset()
        self.assertEqual("enigma", m.compute("hlcqpw"))

    def test_compute_two_scramblers_and_plugboard(self):
        s1 = Scrambler("uwygadfpvzbeckmthxslrinqoj")
        s2 = Scrambler("joqnirlsxhtmkcebzvpfdagywu", "zyxwvutsrqponmlkjihgfedcba")
        r = Reflector("yruhqsldpxngokmiebfzcwvjat")
        p = Plugboard("enma", "gwzk")
        m = Machine(r, p, s1, s2)

        self.assertEqual("zjcntm", m.compute("enigma"))
        m.reset()
        self.assertEqual("enigma", m.compute("zjcntm"))

    def test_send_tick(self):
        s1 = Scrambler("uwygadfpvzbeckmthxslrinqoj")
        s2 = Scrambler("joqnirlsxhtmkcebzvpfdagywu")
        s3 = Scrambler("jnmysrqdklitczueawhvgbxofp")
        r = Reflector("yruhqsldpxngokmiebfzcwvjat")
        p = Plugboard("", "")
        m = Machine(r, p, s1, s2, s3)

        for i in range(0, 26):
            m.send_tick()

        self.assertEqual(0, m.scramblers[0].current_shift)
        self.assertEqual(1, m.scramblers[1].current_shift)
        self.assertEqual(0, m.scramblers[2].current_shift)

        m.reset()
        for i in range(0, 676):
            m.send_tick()

        self.assertEqual(0, m.scramblers[0].current_shift)
        self.assertEqual(0, m.scramblers[1].current_shift)
        self.assertEqual(1, m.scramblers[2].current_shift)

        m.reset()
        for i in range(0, 5401):
            m.send_tick()

        self.assertEqual(19, m.scramblers[0].current_shift)
        self.assertEqual(25, m.scramblers[1].current_shift)
        self.assertEqual(7, m.scramblers[2].current_shift)
