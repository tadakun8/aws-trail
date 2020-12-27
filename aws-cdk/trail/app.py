#!/usr/bin/env python3

from aws_cdk import core

from trail.trail_stack import TrailStack


app = core.App()
TrailStack(app, "trail")

app.synth()
