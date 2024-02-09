{
    "name": "Estate",  # The name that will appear in the App list
    "version": "17.0.0.1",  # Version
    "depends": ["base"],  # dependencies
    "installable": True,
    "application": True, # This line says the module is an App, and not a module
    "license": "LGPL-3",
    'category': 'Sales',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
    ],
    "demo": [
        "data/estate_demo.xml"
    ]    
}
