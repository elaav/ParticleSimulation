import unittest

from src.particle_parse import parse_emc_data, parse_ms_data, parse_ms_coords, separate_events


class ParsingTestCase(unittest.TestCase):

    def test_parse_ms_coords_k_short(self):
        events_text = separate_events('resources/k-short_out.txt', 'k-short')
        # [x, dx, y, dy, z, dz, phi, dphi, [tracks]]
        real_ms_coords = [
            [],
            [],
            [
                ['17.65162', '0.30871', '-1.94957', '0.03000', '-0.36299', '0.72016', '0.14077', '0.00348', [1,2]],
                ['17.41664', '0.31487', '-1.91813', '0.03064', '0.09464', '0.72294', '0.13931', '0.00349', [1,3]],
                ['29.75094', '11.49536', '-2.28033', '0.73339', '1.96355', '1.46304', '0.00231', '0.09430', [2,3]],
            ],
            [],
            []
        ]
        ms_coords = []
        for event in events_text:
            lines = event.split('\n')
            ms_coords.append(parse_ms_coords(lines))

        self.assertEqual(real_ms_coords, ms_coords)

    def test_parse_ms_data_k_short(self):
        events_text = separate_events('resources/k-short_out.txt', 'k-short')
        # [kappa, kappa_err, tandip, tandip_err]
        real_ms_data = [
            [],
            [],
            [
                ['0.595086196E-03', '0.19559E-09', '-0.018603507', '0.30799E-03'],
                ['-0.290886243E-02','0.29021E-09', '0.162233189', '0.40941E-03'],
                ['-0.287601352E-02', '0.29036E-09', '0.166146368', '0.40951E-03'],
            ],
            [],
            []
        ]
        ms_data = []
        for event in events_text:
            lines = event.split('\n')
            ms_data.append(parse_ms_data(lines))

        self.assertEqual(real_ms_data, ms_data)

    def test_parse_emc_data_k_short(self):
        events_text = separate_events('resources/k-short_out.txt', 'k-short')
        # [ph, x, dx, y, dy, z, dz]
        real_emc_data = [
            [
                ['58.0', '133.0', '6.5', '-19.3', '0.5', '6.3', '0.5'],
                ['73.0', '133.0', '6.5', '13.2', '0.4', '-5.3', '0.4'],
                ['23.0', '133.0', '6.5', '-3.0', '0.5', '-3.7', '0.5'],
                ['12.0', '133.0', '6.5', '-7.0', '0.6', '-8.0', '0.6'],
            ],
            [
                ['81.0', '133.0', '6.5', '-10.9', '0.5', '-3.9', '0.5'],
                ['78.0', '133.0', '6.5', '14.8', '0.4', '5.2', '0.4'],
                ['9.0', '133.0', '6.5', '9.0', '0.6', '-12.0', '0.6'],
            ],
            [
                ['11.0','133.0','6.5','-9.0','0.6','-2.0','0.6']
            ],
            [
                ['82.0', '133.0', '6.5', '-3.5', '0.4', '-7.7', '0.4'],
                ['59.0', '133.0', '6.5', '1.2', '0.4', '1.8', '0.4'],
            ],
            [
                ['86.0', '133.0', '6.5', '6.9', '0.4', '-4.5', '0.4'],
                ['45.6', '133.0', '6.5', '-3.1', '0.5', '6.1', '0.5'],
                ['21.0', '133.0', '6.5', '-13.4', '0.5', '0.0', '0.5'],
                ['13.4', '133.0', '6.5', '-1.1', '0.6', '2.1', '0.6'],
            ]
        ]
        emc_data = []
        for event in events_text:
            lines = event.split('\n')
            emc_data.append(parse_emc_data(lines))

        self.assertEqual(real_emc_data, emc_data)