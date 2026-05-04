import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-account-currency-revaluation",
    description="Meta package for open-synergy-ssi-account-currency-revaluation Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_account_currency_revaluation',
        'odoo14-addon-ssi_account_currency_revaluation_operating_unit',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
