# -*- coding: utf-8 -*-
{
    'name': u"URLs Management for Philmer and Family",
    'summary': "Manage URLs of the Philmer's family",
    'description':"""
Manage URLs for Philmer's family
""",
    'depends': ['base',],
    'data': ['security/philmer_urls_security.xml',
             'views/philmer_url_view.xml',
             'views/philmer_url_tag_view.xml',
             'security/ir.model.access.csv',
            ],
    'version':'1.0',
    'application':True,
    'installable': True,
    'auto_install': False,
}
