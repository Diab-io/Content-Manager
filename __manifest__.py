{
    'name': 'Articles',
    'author': 'Odimayo David',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],

    'depends': ['contacts', 'portal'],
}