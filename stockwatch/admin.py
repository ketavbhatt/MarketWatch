# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Stock,tempUser,wishlist


admin.site.register(tempUser)
admin.site.register(Stock)
admin.site.register(wishlist)

# Register your models here.
