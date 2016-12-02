COMMENT

   **************************************************
   File generated by: neuroConstruct v1.7.1 
   **************************************************

   This file holds the implementation in NEURON of the Cell Mechanism:
   ElectSyn (Type: Gap junction, Model: Template based ChannelML file)

   with parameters: 
   /channelml/@units = Physiological Units 
   /channelml/notes = ChannelML file describing a single synaptic mechanism 
   /channelml/synapse_type/@name = ElectSyn 
   /channelml/synapse_type/status/@value = stable 
   /channelml/synapse_type/status/contributor/name = Padraig Gleeson 
   /channelml/synapse_type/notes = Description of an electrical synapse at a gap junction 
   /channelml/synapse_type/electrical_syn/@conductance = 5e-8 

// File from which this was generated: /home/padraig/nC_projects/Gaps/cellMechanisms/ElectSyn/ElectSyn.xml

// XSL file with mapping to simulator: /home/padraig/nC_projects/Gaps/cellMechanisms/ElectSyn/ChannelML_v1.8.1_NEURONmod.xsl

ENDCOMMENT


?  This is a NEURON mod file generated from a ChannelML file

?  Unit system of original ChannelML file: Physiological Units

COMMENT
    ChannelML file describing a single synaptic mechanism
ENDCOMMENT

? Creating synaptic mechanism for an electrical synapse
    

TITLE Channel: ElectSyn

COMMENT
    Description of an electrical synapse at a gap junction
ENDCOMMENT


UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
}

    
NEURON {
    POINT_PROCESS ElectSyn
    NONSPECIFIC_CURRENT i
    RANGE g, i
    RANGE weight
    
    RANGE vgap     : Using a RANGE variable as opposed to POINTER for parallel mode
        

}

PARAMETER {
    v (millivolt)
    vgap (millivolt)
    g = 0.000049999999999999996 (microsiemens)
    weight = 1

}


ASSIGNED {
    i (nanoamp)
}

BREAKPOINT {
    i = weight * g * (v - vgap)
} 
