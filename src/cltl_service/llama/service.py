import logging
from typing import List

from cltl.combot.infra.config import ConfigurationManager
from cltl.combot.infra.event import Event, EventBus
from cltl.combot.infra.resource import ResourceManager
from cltl.combot.infra.time_util import timestamp_now
from cltl.combot.infra.topic_worker import TopicWorker
from cltl.llama.api import Llama
from cltl.combot.event.emissor import TextSignalEvent
from cltl_service.emissordata.client import EmissorDataClient
from emissor.representation.scenario import TextSignal

logger = logging.getLogger(__name__)

CONTENT_TYPE_SEPARATOR = ';'


class LlamaService:
    @classmethod
    def from_config(cls, llama: Llama, emissor_client: EmissorDataClient,
                    event_bus: EventBus, resource_manager: ResourceManager,
                    config_manager: ConfigurationManager):
        config = config_manager.get_config("cltl.llama")

        input_topic = config.get("topic_input")
        output_topic = config.get("topic_output")

        intention_topic = config.get("topic_intention") if "topic_intention" in config else None
        intentions = config.get("intentions", multi=True) if "intentions" in config else []

        language = config.get("language")
        port = config.get("port")
        llama._language = language
        llama._port = port
        return cls(input_topic, output_topic,
                   intention_topic, intentions,
                   llama, emissor_client, event_bus, resource_manager)

    def __init__(self, input_topic: str, output_topic: str,
                 intention_topic: str, intentions: List[str],
                 llama: Llama, emissor_client: EmissorDataClient,
                 event_bus: EventBus, resource_manager: ResourceManager):
        self._llama = llama
        self._event_bus = event_bus
        self._resource_manager = resource_manager
        self._emissor_client = emissor_client

        self._input_topic = input_topic
        self._output_topic = output_topic
        self._intentions = intentions if intentions else ()
        self._intention_topic = intention_topic if intention_topic else None

        self._topic_worker = None

    #     def __init__(self, input_topic: str, output_topic: str,
    #                  intention_topic: str, intentions: List[str],
    #                  llama: Llama, emissor_client: EmissorDataClient,
    #                  event_bus: EventBus, resource_manager: ResourceManager, language: str, port:str):
    #         self._llama = llama
    #         self._llama._language = language
    #         self._llama._port = port
    #         self._event_bus = event_bus
    #         self._resource_manager = resource_manager
    #         self._emissor_client = emissor_client
    #
    #         self._input_topic = input_topic
    #         self._output_topic = output_topic
    #         self._intentions = intentions if intentions else ()
    #         self._intention_topic = intention_topic if intention_topic else None
    #
    #         self._topic_worker = None

    @property
    def app(self):
        return None

    def start(self, timeout=30):
        self._topic_worker = TopicWorker([self._input_topic, self._intention_topic], self._event_bus,
                                         provides=[self._output_topic],
                                         intention_topic=self._intention_topic, intentions=self._intentions,
                                         resource_manager=self._resource_manager, processor=self._process,
                                         name=self.__class__.__name__)
        self._topic_worker.start().wait()

    def stop(self):
        if not self._topic_worker:
            pass

        self._topic_worker.stop()
        self._topic_worker.await_stop()
        self._topic_worker = None

    def _process_org(self, event: Event[TextSignalEvent]):
        if self._is_llama_intention(event):
            greeting_payload = self._create_payload(self._llama.respond(None))
            self._event_bus.publish(self._output_topic, Event.for_payload(greeting_payload))
        elif event.metadata.topic == self._input_topic:
            response = self._llama.respond(event.payload.signal.text)

            if response:
                llama_event = self._create_payload(response)
                self._event_bus.publish(self._output_topic, Event.for_payload(llama_event))

    def _process(self, event: Event[TextSignalEvent]):
        if event.metadata.topic == self._input_topic:
            response = self._llama._analyze(event.payload.signal.text)
            if response:
                llama_event = self._create_payload(response)
                self._event_bus.publish(self._output_topic, Event.for_payload(llama_event))

    def _create_payload(self, response):
        scenario_id = self._emissor_client.get_current_scenario_id()
        signal = TextSignal.for_scenario(scenario_id, timestamp_now(), timestamp_now(), None, response)

        return TextSignalEvent.for_agent(signal)

    def _is_llama_intention(self, event):
        return (event.metadata.topic == self._intention_topic
                and hasattr(event.payload, "intentions")
                and any(intention.label in self._intentions for intention in event.payload.intentions))
