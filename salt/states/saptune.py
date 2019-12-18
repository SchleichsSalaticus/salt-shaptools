'''
State module to provide Saptune functionality to Salt

.. versionadded:: pending

:maintainer:    Dario Maiocchi <dmaiocchi@suse.com>
:maturity:      alpha
:depends:       saptune
:platform:      all

:configuration: This module requires the saptune python module and uses the
    following defaults which may be overridden in the minion configuration:

.. code-block:: yaml

:usage:

.. code-block:: yaml
  solution_is_removed:
    saptune.solution_is_absent:
        - name: HANA
        (option to apply multiple solution)
        - solutions:
            - solution1
            - solution2
'''


# Import python libs
from __future__ import absolute_import, unicode_literals, print_function


# Import salt libs
from salt import exceptions
from salt.ext import six


__virtualname__ = 'saptune'

def __virtual__():  # pragma: no cover
    '''
    Only load if the saptune module is in __salt__
    '''
    return 'saptune.apply_solution' in __salt__


def solution_applied(name):
    """
    Apply a saptune solution
    """
    ret = {'name': name,
           'changes': {},
           'result': False,
           'comment': ''}

    if __salt__['saptune.apply_solution'](solution_name=name):
        ret['result'] = True
        ret['comment'] = 'Saptune solution is already applied'
        return ret

    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = 'Saptune {} solution would be applied'.format(name)
        ret['changes']['name'] = name
        return ret

    try:
        #  Here starts the actual process
        result = __salt__['saptune.apply_solution'](solution_name=name)

        if result:
            ret['changes']['name'] = name
            ret['comment'] = 'Error appling saptune solution'
            ret['result'] = False
            return ret

        ret['changes']['name'] = name
        ret['comment'] = 'Saptune solution applied'
        ret['result'] = True
        return ret

    except exceptions.CommandExecutionError as err:
        ret['comment'] = six.text_type(err)
        return ret
