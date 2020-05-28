c ----------------------------------------------------------------------------
c    MCNP-Model for cross section calculations
c                                                                               
c     - Blaine Heffron                                       
c     - March 13, 2020                                                           
c     - Neutrino Physics Group, ORNL                                              
c     - updated May 22, 2020 - use a thin cylinder
c                                                                               
c   Description of simulation: 4mx4mx4m block of material with neutron gun      
c     shooting 100k neutrons into volume originating 1m in the block
c                                                                               
c ----------------------------------------------------------------------------  
c CELL CARDS    
  100 1 -%(density)s -100         $ material density in g/cc
  900 0 -900 #100 
  999 0 900  
c END CELL CARD - BLANK LINE FOLLOWS                                          

c SURFACE CARDS 
c 100 box -600 -600 -600 1200 0 0 0 1200 0 0 0 1200  
  100 rcc -250 0 0 500 0 0 0.001
c Rest of universe -----------------------------------------------------------  
c 900 box -601 -601 -601 1202 0 0 0 1202 0 0 0 1202 
  900 rcc -251 0 0 502 0 0 0.0011
c END SURFACE CARD - BLANK LINE FOLLOWS                                         
                                                         
c DATA CARDS                                                                    
mode  n p h d t a e s
c random number seed
RAND  GEN=2 SEED=%(seed)s STRIDE=152917
c MODEL PHYSICS
MPHYS ON
c MATERIAL SPECIFICATION
M1 %(matnum)s 1.0           $ Material used
c VARIANCE REDUCTION                                                            
imp:N   1 0 0           
c Single energy neutron
SDEF ERG=%(energy)s POS=-249.9 0 0 PAR=n DIR=1 VEC=1 0 0                 
nps  %(nevts)s                                                                   
phys:n J 100. 0 J J J 0.0 -1 0 $ use analog capture for these sims
c phys:n J 100. 0 J J J 3.002 -1 0 $ use analog capture for these sims
c phys:p J 1 1 J J J J 
c ACT nonfission=ALL DN=BOTH DG=LINES
c first parameter on cut cards is the time in shakes it tracks the particle
cut:N 20E8   $ neutron, 20 seconds is plenty to traverse 50 m of material at .01 MeV ~ 6.5m/s
c cut:P 1E16 1E-3   $ photon                                                                 
c cut:E 1E16 0  $ electron                                                         
c cut:H 1E16 0  $ proton                                                           
c cut:A 1E16 0  $ alpha
c cut:S 1E16 0  $ 3Helium
c cut:D 1E16 0  $ deuteron
c cut:T 1E16 0  $ triton
c particle track specification
c MEPH 1 means only 1 event per history, write all writes direction cosines, 
c TYPE=N restricts written events to neutrons only
PTRAC MAX=%(nevts_max)s MEPH=3 WRITE=ALL FILE=ASC $ TYPE=N 
