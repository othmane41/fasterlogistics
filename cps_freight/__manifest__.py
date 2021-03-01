# See LICENSE file for full copyright and licensing details.

{
    # Module Info.
    "name": "Freight Management",
    "version": "13.0.1.0.0",
    "sequence": 1,
    "category": "Transport",
    "license": 'LGPL-3',
    "summary": """Freight Management System for Carriers, Transport,
                  Goods Import/Export, Shipping and
                  Transportation Solutions,
                  Freight Management Software.""",
    "description": """Freight Management System for Carriers, Transport,
                      Goods Import/Export, Shipping and
                      Transportation Solutions,
                      Freight Management Software.""",

    # Author
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",

    # Dependencies
    "depends": ['product', 'account'],

    # Data
    "data": [
        'data/ir_sequence_data.xml',
        'views/cps_colisage.xml',
        'views/cps_trajet.xml',
        'views/cps_soustraitant.xml',
        'views/cps_voyage_tracking.xml',
        'views/cps_voyage_resume.xml',
        'views/cps_voyage.xml',
        'views/fleet_vehicle.xml',
        'views/res_partner.xml',
        'views/cps_menu.xml',
        'security/ir.model.access.csv'
    ],

    # Odoo App Store Specific
    'images': ['static/description/odoo-app-freight.jpg'],

    # Technical
    "application": True,
    "installable": True,
    'price': 80,
    'currency': 'EUR',
}
