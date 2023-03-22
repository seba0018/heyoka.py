# Copyright 2020, 2021, 2022, 2023 Francesco Biscani (bluescarni@gmail.com), Dario Izzo (dario.izzo@gmail.com)
#
# This file is part of the heyoka.py library.
#
# This Source Code Form is subject to the terms of the Mozilla
# Public License v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest as _ut


class model_test_case(_ut.TestCase):
    def test_mascon(self):
        from . import (
            model,
            make_vars,
            expression as ex,
            sum_sq,
            sqrt,
            sum as hysum,
            par,
        )

        x, y, z, vx, vy, vz = make_vars("x", "y", "z", "vx", "vy", "vz")

        dyn = model.mascon(
            Gconst=1.5, masses=[1.1], positions=[[1.0, 2.0, 3.0]], omega=[0.0, 0.0, 3.0]
        )

        self.assertEqual(dyn[0][0], x)
        self.assertEqual(dyn[0][1], ex("vx"))

        tmp = 1.5 * ((1.0 - x) * (1.1 * (sum_sq([1.0 - x, 2.0 - y, 3.0 - z])) ** -1.5))
        tmp = tmp + hysum([9.0000000000000000 * x, 6.0000000000000000 * vy])

        self.assertEqual(
            dyn[3][1],
            tmp,
        )

        pot = model.mascon_potential(
            Gconst=1.5, masses=[1.1], positions=[[1.0, 2.0, 3.0]], omega=[0.0, 0.0, 3.0]
        )

        tmp = -1.5 * (1.1 / sqrt(sum_sq([1.0 - x, 2.0 - y, 3.0 - z])))
        tmp = tmp + 0.50000000000000000 * (
            (3.0000000000000000 * z) ** 2 - (9.0000000000000000 * sum_sq([x, y, z]))
        )

        self.assertEqual(pot, tmp)

        en = model.mascon_energy(
            Gconst=1.5, masses=[1.1], positions=[[1.0, 2.0, 3.0]], omega=[0.0, 0.0, 3.0]
        )

        self.assertGreater(len(en), len(pot))

        with self.assertRaises(ValueError) as cm:
            model.mascon(
                Gconst=1.5,
                masses=[1.1],
                positions=[1.0, 2.0, 3.0],
                omega=[0.0, 0.0, 3.0],
            )
        self.assertTrue(
            "Invalid positions array in a mascon model: the number of dimensions must be 2, but it is 1 instead"
            in str(cm.exception)
        )

        with self.assertRaises(ValueError) as cm:
            model.mascon(
                Gconst=1.5,
                masses=[1.1],
                positions=[[1.0, 2.0, 3.0, 4.0]],
                omega=[0.0, 0.0, 3.0],
            )
        self.assertTrue(
            "Invalid positions array in a mascon model: the number of columns must be 3, but it is 4 instead"
            in str(cm.exception)
        )

        with self.assertRaises(TypeError) as cm:
            model.mascon(
                Gconst=1.5,
                masses=[1.1],
                positions=[[{}, {}, {}]],
                omega=[0.0, 0.0, 3.0],
            )
        self.assertTrue(
            "The positions array in a mascon model could not be converted into an array of expressions - please make sure that the array's values can be converted into heyoka expressions"
            in str(cm.exception)
        )

        # Run also a test with parametric mass.
        dyn = model.mascon(
            Gconst=1.5,
            masses=[par[0]],
            positions=[[1.0, 2.0, 3.0]],
            omega=[0.0, 0.0, 3.0],
        )

        tmp = 1.5 * (
            (1.0 - x) * (par[0] * (sum_sq([1.0 - x, 2.0 - y, 3.0 - z])) ** -1.5)
        )
        tmp = tmp + hysum([9.0000000000000000 * x, 6.0000000000000000 * vy])

        self.assertEqual(
            dyn[3][1],
            tmp,
        )

    def test_rotating(self):
        from . import model, make_vars, expression as ex, sum as hysum, sum_sq

        x, y, z, vx, vy, vz = make_vars("x", "y", "z", "vx", "vy", "vz")

        dyn = model.rotating(omega=[0.0, 0.0, 3.0])

        self.assertEqual(dyn[0][0], x)
        self.assertEqual(dyn[0][1], ex("vx"))

        self.assertEqual(
            dyn[3][1], hysum([9.0000000000000000 * x, 6.0000000000000000 * vy])
        )

        pot = model.rotating_potential([0.0, 0.0, 3.0])

        tmp = 0.50000000000000000 * (
            (3.0000000000000000 * z) ** 2 - (9.0000000000000000 * sum_sq([x, y, z]))
        )

        self.assertEqual(pot, tmp)

        en = model.rotating_energy([0.0, 0.0, 3.0])

        self.assertEqual(en, 0.5 * sum_sq([vx, vy, vz]) + tmp)

    def test_fixed_centres(self):
        from . import model, make_vars, expression as ex, sum_sq, sqrt

        x, y, z, vx, vy, vz = make_vars("x", "y", "z", "vx", "vy", "vz")

        dyn = model.fixed_centres(Gconst=1.5, masses=[1.1], positions=[[1.0, 2.0, 3.0]])

        self.assertEqual(dyn[0][0], x)
        self.assertEqual(dyn[0][1], ex("vx"))

        tmp = 1.5 * ((1.0 - x) * (1.1 * (sum_sq([1.0 - x, 2.0 - y, 3.0 - z])) ** -1.5))

        self.assertEqual(
            dyn[3][1],
            tmp,
        )

        en = model.fixed_centres_energy(
            Gconst=1.5, masses=[1.1], positions=[[1.0, 2.0, 3.0]]
        )

        self.assertEqual(
            en,
            0.5 * sum_sq([vx, vy, vz])
            + -1.5 * (1.1 / sqrt(sum_sq([1.0 - x, 2.0 - y, 3.0 - z]))),
        )

        pot = model.fixed_centres_potential(
            Gconst=1.5, masses=[1.1], positions=[[1.0, 2.0, 3.0]]
        )

        self.assertEqual(
            pot,
            -1.5 * (1.1 / sqrt(sum_sq([1.0 - x, 2.0 - y, 3.0 - z]))),
        )

        with self.assertRaises(ValueError) as cm:
            model.fixed_centres(Gconst=1.5, masses=[1.1], positions=[1.0, 2.0, 3.0])
        self.assertTrue(
            "Invalid positions array in a fixed centres model: the number of dimensions must be 2, but it is 1 instead"
            in str(cm.exception)
        )

        with self.assertRaises(ValueError) as cm:
            model.fixed_centres(
                Gconst=1.5, masses=[1.1], positions=[[1.0, 2.0, 3.0, 4.0]]
            )
        self.assertTrue(
            "Invalid positions array in a fixed centres model: the number of columns must be 3, but it is 4 instead"
            in str(cm.exception)
        )

        with self.assertRaises(TypeError) as cm:
            model.fixed_centres(Gconst=1.5, masses=[1.1], positions=[[{}, {}, {}]])
        self.assertTrue(
            "The positions array in a fixed centres model could not be converted into an array of expressions - please make sure that the array's values can be converted into heyoka expressions"
            in str(cm.exception)
        )

    def test_nbody(self):
        from . import model, expression, sqrt, sum_sq, make_vars

        dyn = model.nbody(2, masses=[0.0, 0.0])

        self.assertEqual(len(dyn), 12)

        self.assertEqual(dyn[3][1], expression(0.0))
        self.assertEqual(dyn[4][1], expression(0.0))
        self.assertEqual(dyn[5][1], expression(0.0))

        self.assertEqual(dyn[9][1], expression(0.0))
        self.assertEqual(dyn[10][1], expression(0.0))
        self.assertEqual(dyn[11][1], expression(0.0))

        dyn = model.nbody(2, Gconst=5.0)

        self.assertTrue("5.0000000000000" in str(dyn[3][1]))
        self.assertTrue("5.0000000000000" in str(dyn[4][1]))
        self.assertTrue("5.0000000000000" in str(dyn[5][1]))

        self.assertTrue("5.0000000000000" in str(dyn[9][1]))
        self.assertTrue("5.0000000000000" in str(dyn[10][1]))
        self.assertTrue("5.0000000000000" in str(dyn[11][1]))

        en = model.nbody_energy(2, masses=[0.0, 0.0])

        self.assertEqual(en, expression(0.0))

        en = model.nbody_energy(2, Gconst=5.0)

        self.assertTrue("5.0000000000000" in str(en))

        x0, y0, z0, x1, y1, z1 = make_vars("x_0", "y_0", "z_0", "x_1", "y_1", "z_1")

        self.assertEqual(
            model.nbody_potential(2),
            -(1.0000000000000000 / sqrt(sum_sq([x1 - x0, y1 - y0, z1 - z0]))),
        )

        dyn = model.np1body(2, masses=[0.0, 0.0])

        self.assertEqual(len(dyn), 6)

        self.assertEqual(dyn[3][1], expression(0.0))
        self.assertEqual(dyn[4][1], expression(0.0))
        self.assertEqual(dyn[5][1], expression(0.0))

        dyn = model.np1body(2, Gconst=5.0)

        self.assertTrue("10.0000000000000" in str(dyn[3][1]))
        self.assertTrue("10.0000000000000" in str(dyn[4][1]))
        self.assertTrue("10.0000000000000" in str(dyn[5][1]))

        en = model.np1body_energy(2, masses=[])

        self.assertEqual(en, expression(0.0))

        en = model.np1body_energy(2, Gconst=5.0)

        self.assertTrue("5.0000000000000" in str(en))

        self.assertEqual(
            model.np1body_potential(2),
            -(1.0000000000000000 / sqrt(sum_sq([x1, y1, z1]))),
        )

    def test_pendulum(self):
        from . import model, expression, make_vars, sin, cos

        x, v = make_vars("x", "v")

        dyn = model.pendulum()

        self.assertEqual(dyn[0][0], x)
        self.assertEqual(dyn[0][1], v)
        self.assertEqual(dyn[1][0], v)
        self.assertEqual(dyn[1][1], -sin(x))

        dyn = model.pendulum(gconst=2.0)

        self.assertEqual(dyn[0][0], x)
        self.assertEqual(dyn[0][1], v)
        self.assertEqual(dyn[1][0], v)
        self.assertEqual(dyn[1][1], -2.0 * sin(x))

        dyn = model.pendulum(gconst=4.0, l=2.0)

        self.assertEqual(dyn[0][0], x)
        self.assertEqual(dyn[0][1], v)
        self.assertEqual(dyn[1][0], v)
        self.assertEqual(dyn[1][1], -2.0 * sin(x))

        en = model.pendulum_energy()

        self.assertEqual(
            en, ((0.50000000000000000 * v**2) + (1.0000000000000000 - cos(x)))
        )

        en = model.pendulum_energy(gconst=2.0)

        self.assertEqual(
            en,
            (
                (0.50000000000000000 * v**2)
                + (2.0000000000000000 * (1.0000000000000000 - cos(x)))
            ),
        )

        en = model.pendulum_energy(l=2.0, gconst=4.0)

        self.assertEqual(
            en,
            (
                (
                    (2.0000000000000000 * v**2)
                    + (8.0000000000000000 * (1.0000000000000000 - cos(x)))
                )
            ),
        )
