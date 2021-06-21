CONTIKI_PROJECT = node
all: $(CONTIKI_PROJECT)

PLATFORMS_EXCLUDE = sky nrf52dk native

CONTIKI=../../..

# RPL storing mode?
MAKE_WITH_STORING_ROUTING ?= 0

 # force Orchestra from command line
MAKE_WITH_ORCHESTRA ?= 0

MAKE_MAC = MAKE_MAC_TSCH

ifeq ($(MAKE_WITH_ORCHESTRA),1)
  MODULES += $(CONTIKI_NG_SERVICES_DIR)/orchestra

  ifeq ($(MAKE_WITH_STORING_ROUTING),1)
    ifeq ($(MAKE_WITH_LINK_BASED_ORCHESTRA),1)
      # enable the `link_based` rule
      CFLAGS += -DORCHESTRA_CONF_RULES="{&eb_per_time_source,&unicast_per_neighbor_link_based,&default_common}"
    else
      # enable the `rpl_storing` rule
      CFLAGS += -DORCHESTRA_CONF_RULES="{&eb_per_time_source,&unicast_per_neighbor_rpl_storing,&default_common}"
    endif
  else
    ifeq ($(MAKE_WITH_LINK_BASED_ORCHESTRA),1)
      $(error "Inconsistent configuration")
    endif
  endif
endif

ifeq ($(MAKE_WITH_STORING_ROUTING),1)
  MAKE_ROUTING = MAKE_ROUTING_RPL_CLASSIC
  CFLAGS += -DRPL_CONF_MOP=RPL_MOP_STORING_NO_MULTICAST
endif


#MAKE_ROUTING = MAKE_ROUTING_RPL_CLASSIC

# Energy usage estimation
MODULES += os/services/simple-energest

include $(CONTIKI)/Makefile.dir-variables
include $(CONTIKI)/Makefile.include
