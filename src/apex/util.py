# These imports are for python3 compatibility inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import click


def echo_colorized_frame(frame, port_name, direction_in):
    formatted_aprs = '>'.join([click.style(frame['source'], fg='green'), click.style(frame['destination'], fg='blue')])
    paths = []
    for path in frame['path']:
        paths.append(click.style(path, fg='cyan'))
    paths = ','.join(paths)
    if frame['path']:
        formatted_aprs = ','.join([formatted_aprs, paths])
    formatted_aprs += ':'
    formatted_aprs += frame['text']
    if direction_in:
        click.echo(click.style(port_name + ' << ', fg='magenta') + formatted_aprs)
    else:
        click.echo(click.style(port_name + ' >> ', fg='magenta', bold=True, blink=True) + formatted_aprs)

def echo_colorized_error(text):
    click.echo(click.style('Error: ', fg='red', bold=True, blink=True) + click.style(text, bold=True))

def echo_colorized_warning(text):
    click.echo(click.style('Error: ', fg='yellow') + click.style(text))
