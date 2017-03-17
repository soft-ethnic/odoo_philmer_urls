# -*- encoding: utf-8 -*-
import time
from openerp import tools
from openerp import models, fields, api, _
from openerp.exceptions import Warning
import logging

_logger = logging.getLogger(__name__)

class philmer_url_tag(models.Model):
    _name = 'philmer.url.tag'
    _description = 'URLs Tags'
    _order = 'name'
    
    name = fields.Char('Name', required=True)
    url_ids = fields.Many2many('philmer.url', relation='philmer_urls_tags', column1='tag_id', column2='url_id', string='URLs')
    active = fields.Boolean('Active', default=True)

