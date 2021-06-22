from typing import Optional, Text

from tfx import types
from tfx.dsl.components.base import base_component
from tfx.dsl.components.base import executor_spec
from executor import UndersamplingExecutor
from tfx.types import channel_utils
from tfx.types import standard_artifacts
from tfx.types.component_spec import ChannelParameter
from tfx.types.component_spec import ExecutionParameter


class UndersamplingComponentSpec(types.ComponentSpec):

  PARAMETERS = {
      # These are parameters that will be passed in the call to
      # create an instance of this component.
      'name': ExecutionParameter(type=Text, optional=True),
  }
  INPUTS = {
      # This will be a dictionary with input artifacts, including URIs
      'input_data': ChannelParameter(type=standard_artifacts.Examples),
  }
  OUTPUTS = {
      # This will be a dictionary which this component will populate
      'output_data': ChannelParameter(type=standard_artifacts.Examples),
  }


class UndersamplingComponent(base_component.BaseComponent):
  SPEC_CLASS = UndersamplingComponentSpec
  EXECUTOR_SPEC = executor_spec.ExecutorClassSpec(UndersamplingExecutor)

  def __init__(self,
               input_data: types.Channel = None,
               output_data: types.Channel = None,
               name: Optional[Text] = None):

    """Construct a HelloComponent.
    Args:
      input_data: A Channel of type `standard_artifacts.Examples`. This will
        often contain two splits: 'train', and 'eval'.
      output_data: A Channel of type `standard_artifacts.Examples`. This will
        usually contain the same splits as input_data.
      name: Optional unique name. Necessary if multiple components are
        declared in the same pipeline.
    """
    # output_data will contain a list of Channels for each split of the data,
    # by default a 'train' split and an 'eval' split. Since HelloComponent
    # passes the input data through to output, the splits in output_data will
    # be the same as the splits in input_data, which were generated by the
    # upstream component.
    if not output_data:
      output_data = channel_utils.as_channel([standard_artifacts.Examples()])

    spec = UndersamplingComponentSpec(input_data=input_data,
                              output_data=output_data, name=name)
    super(UndersamplingComponent, self).__init__(spec=spec)
