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
c first parameter on cut cards is the time in shakes it tracks the particle
cut:N 2E8   $ neutron, 2 seconds is plenty to traverse 5 m of material at .01 MeV ~ 6.5m/s
PTRAC MAX=%(nevts_max)s MEPH=3 WRITE=ALL FILE=ASC $ TYPE=N 
