#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#@File : tp2_decoration.py
#@auteur : Junxi ZHANG
#@date : 04/11/2020
#@description : Affaire avec RSA


from inspect import signature
from functools import wraps


#class Detection
class Detection(object):
    """Class de détection des paramètres."""

    def __init__(self):
        super().__init__()

    def type_alerte(*ty_args, **ty_kwargs):
        """Vérification du type de paramètre."""

        def decorate(func):
            sig = signature(func)
            bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments
            @wraps(func)
            def wrapper(*args, **kwargs):
                bound_values = sig.bind(*args, **kwargs).arguments
                for name, value in bound_values.items():
                    if name in bound_types:
                        if not isinstance(value, bound_types[name]):
                            raise TypeError(
                            'Argument {} doit être {}'.format(name,bound_types[name])
                            )
                return func(*args, **kwargs)
            return wrapper
        return decorate

    def type_exclure_alerte(*ty_args, **ty_kwargs):
        """Vérification du type de paramètre."""

        def decorate(func):
            sig = signature(func)
            bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments
            @wraps(func)
            def wrapper(*args, **kwargs):
                bound_values = sig.bind(*args, **kwargs).arguments
                for name, value in bound_values.items():
                    if name in bound_types:
                        if isinstance(value, bound_types[name]):
                            raise TypeError(
                            'Argument {} ne doit pas être {}'.format(name,bound_types[name])
                            )
                return func(*args, **kwargs)
            return wrapper
        return decorate

    def valeur_alerte(*ty_args, **ty_kwargs):
        """Vérification de la valeur de paramètre."""

        def decorate(func):
            sig = signature(func)
            bound_conditions = sig.bind_partial(*ty_args, **ty_kwargs).arguments
            @wraps(func)
            def wrapper(*args, **kwargs):
                bound_values= sig.bind(*args, **kwargs).arguments

                #Attribuer des valeurs aux conditions pour faciliter le jugement de eval()
                bound_conditions_temp ={}
                for name, bound_condition in bound_conditions.items():
                    for param_name, value in bound_values.items():
                        bound_condition = bound_condition.replace(param_name,str(value))
                    bound_conditions_temp[name] = bound_condition

                for name, value in bound_values.items():
                    if name in bound_conditions_temp:
                        if not eval(bound_conditions_temp[name]):
                            raise ValueError(
                            'Argument {} doit répondre à la condition {}'.format(name, bound_conditions[name])
                            )
                return func(*args, **kwargs)
            return wrapper
        return decorate


#class Singleton
class Singleton(object):
    """Assurant que la classe actuelle est singleton."""

    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]
