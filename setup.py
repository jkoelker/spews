#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools as st

st.setup(name='spew',
         packages=st.find_packages(),
         entry_points={
            'afew.filter': [
                'DistributionFilter= spew.distribution:DistributionFilter',
                'StickyFilter = spew.sticky:StickyFilter',
            ],
        },
        install_requires=['afew'],
)
