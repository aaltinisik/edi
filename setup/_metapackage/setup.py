import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-edi",
    description="Meta package for oca-edi Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-account_e-invoice_generate',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
