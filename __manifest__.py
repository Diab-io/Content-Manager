{
    'name': 'Articles',

    'summary': 'create and read articles',

    'description': 'create and read articles',

    'author': 'Odimayo David',
    'website':'https://github.com/Diab-io/content_manager',
    'email':'odimayodavid7@gmail.com',

    'version': '16.0.0.1',
    'license': 'LGPL-3',


    'depends': ['contacts', 'portal'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'report/manager_report.xml',
        'report/report_template.xml',
        'data/mail_template_data.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],


    'installable': True,
    'application': True,
}