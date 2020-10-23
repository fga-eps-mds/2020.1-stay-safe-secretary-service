"""
Available crimes of each secretary.
"""
VALID_CRIMES_DF = [
    'Latrocínio',
    'Roubo a Transeunte',
    'Roubo de Veículo',
    'Roubo de Residência',
    'Furto de Veículo',
    'Estupro',
    'Furto a Transeunte',
]

VALID_CRIMES_SP = [
    'Latrocínio',
    'Estupro',
    'Outros Roubos',
    'Roubo de Veículo',
    'Outros Furtos',
    'Furto de Veículo',
]


"""
The range follows the pattern: 0 -> pos[0], pos[0] -> pos[1], ...
and were calculated based on an annual amount of crimes / 100k inhabitants.
"""
ANNUAL_CRIMES_RANGE = [
    {
        'state': 'df',
        'crimes_range': {
            'Latrocínio': [0, 1, 3, 6, 10],
            'Roubo a Transeunte': [200, 400, 600, 1000, 1500],
            'Roubo de Veículo': [0, 10, 20, 50, 100],
            'Roubo de Residência': [0, 5, 10, 20, 50],
            'Furto de Veículo': [50, 100, 200, 500, 700],
            'Estupro': [20, 30, 40, 50, 70],
            'Furto a Transeunte': [20, 50, 70, 90, 100],
        }
    },
    {
        'state': 'sp',
        'crimes_range': {
            'Latrocínio': [0, 1, 3, 6, 10],
            'Estupro': [20, 30, 40, 50, 70],
            'Outros Roubos': [10, 30, 50, 100, 200],
            'Roubo de Veículo': [0, 10, 20, 50, 100],
            'Outros Furtos': [200, 500, 700, 1000, 1500],
            'Furto de Veículo': [50, 100, 200, 500, 700],
        }
    },
]
