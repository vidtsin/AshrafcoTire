# -*- coding: utf-8 -*-
from odoo import models, fields


class ZkAttendanceConfig(models.TransientModel):
    _name = 'zk.attendance'

    device_id = fields.Many2one('zk.machine', string='Device ID', required=True)

    def download_attendance(self):
        self.device_id.download_attendance()

    def clear_attendance(self):
        self.device_id.clear_attendance()
