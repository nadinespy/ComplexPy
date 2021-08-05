  %% (c) Ilya Nemenman, 2002--2006
  %% Distributed under GPL, version 2
  %% Copyright (2006). The Regents of the University of California.

  %% This material was produced under U.S. Government contract
  %% W-7405-ENG-36 for Los Alamos National Laboratory, which is
  %% operated by the University of California for the U.S.
  %% Department of Energy. The U.S. Government has rights to use,
  %% reproduce, and distribute this software.  NEITHER THE
  %% GOVERNMENT NOR THE UNIVERSITY MAKES ANY WARRANTY, EXPRESS
  %% OR IMPLIED, OR ASSUMES ANY LIABILITY FOR THE USE OF THIS
  %% SOFTWARE.  If software is modified to produce derivative works,
  %% such modified software should be clearly marked, so as not to
  %% confuse it with the version available from LANL.
  %%
  %% Additionally, this program is free software; you can redistribute
  %% it and/or modify it under the terms of the GNU General Public
  %% License as published by the Free Software Foundation; either
  %% version 2 of the License, or (at your option) any later version.
  %% Accordingly, this program is distributed in the hope that it will
  %% be useful, but WITHOUT ANY WARRANTY; without even the implied
  %% warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
  %% See the GNU General Public License for more details.

  order_K = 10;			# number of terms in the series
  B   = zeros(1,order_K);

  ## temporary variables
  EG = - nsbpsi(1);		# euler's gamma
  pg1B0  = polygamma(1, B0);
  pg1NB0 = polygamma(1, N+B0);
  denum  = K1/B0^2 - pg1B0 + pg1NB0; # denumerator
  pg2B0  = polygamma(2, B0);
  pg2NB0 = polygamma(2, N+B0);
  pg21   = polygamma(2,1);
  pg3B0  = polygamma(3, B0);
  pg3NB0 = polygamma(3, N+B0);
  pg4B0  = polygamma(4, B0);
  pg4NB0 = polygamma(4, N+B0);
  pg41   = polygamma(4, 1);
  pg5B0  = polygamma(5, B0);
  pg5NB0 = polygamma(5, N+B0);
  pg51   = polygamma(5, 1);
  pg6B0  = polygamma(6, B0);
  pg6NB0 = polygamma(6, N+B0);
  pg61   = polygamma(6, 1);
  pg7B0  = polygamma(7, B0);
  pg7NB0 = polygamma(7, N+B0);
  pg71   = polygamma(7, 1);
  pg8B0  = polygamma(8, B0);
  pg8NB0 = polygamma(8, N+B0);
  pg81   = polygamma(8, 1);
  pg9B0  = polygamma(9, B0);
  pg9NB0 = polygamma(9, N+B0);
  pg91   = polygamma(9, 1);
  pg10B0 = polygamma(10, B0);
  pg10NB0= polygamma(10, N+B0);
  pg101  = polygamma(10, 1);


  B02    = B0^2;


  f0   = sum(kx(nx>1).*nsbpsi(nx(nx>1)));
  d1f0 = sum(kx(nx>1).*polygamma(1, nx(nx>1)));
  d2f0 = sum(kx(nx>1).*polygamma(2, nx(nx>1)));
  d3f0 = sum(kx(nx>1).*polygamma(3, nx(nx>1)))
  d4f0 = sum(kx(nx>1).*polygamma(4, nx(nx>1)));
  d5f0 = sum(kx(nx>1).*polygamma(5, nx(nx>1)));
  d6f0 = sum(kx(nx>1).*polygamma(6, nx(nx>1)))
  d7f0 = sum(kx(nx>1).*polygamma(7, nx(nx>1)));
  d8f0 = sum(kx(nx>1).*polygamma(8, nx(nx>1)));
  d9f0 = sum(kx(nx>1).*polygamma(9, nx(nx>1)))

  B(1) = (B0^2*(EG*K2 + f0)) / (B0^2*denum);

  B(2) = (K2*pi^2*B0 - (6*K1*B(1)^2)/B0^3 - 3*B(1)^2*pg2B0 + \
	  3*B(1)^2*pg2NB0 - 6*B0*d1f0)/(-6*denum);
  
  B(3) = (K2*pi^2*B(1) + (6*K1*B(1)^3)/B0^4 -(12*K1*B(1)*B(2))/B0^3 + \
	  3*K2*B0^2*pg21 - 6*B(1)*B(2)*pg2B0 + 6*B(1)*B(2)*pg2NB0 - \
	  B(1)^3*pg3B0 + B(1)^3*pg3NB0 - 6*B(1)*d1f0 - 3*B0^2*d2f0)/ \
      (-6*denum);
  
  B(4) = -(-(K2*pi^4*B0^3)/90 + (K1*B(1)^4)/B0^5 - (K2*pi^2*B(2))/6 - \
	   (3*K1*B(1)^2*B(2))/B0^4 + (K1*B(2)^2)/B0^3 + \
	   (2*K1*B(1)*B(3))/B0^3 - K2*B0*B(1)*pg21 + ((B(2)^2 + \
						       2*B(1)*B(3))*pg2B0)/2 \
	   - ((B(2)^2 + 2*B(1)*B(3))*pg2NB0)/2 + \
	   (B(1)^2*B(2)*pg3B0)/2 - (B(1)^2*B(2)*pg3NB0)/2 + \
	   (B(1)^4*pg4B0)/ 24 - (B(1)^4*pg4NB0)/24 +  B(2)*d1f0 + \
	   B0*B(1)*d2f0 + (B0^3*d3f0)/6)/(-denum);
 
  B(5) = (-((B(2)*B(3) + B(1)*B(4))*pg2B0) + (B(2)*B(3) + \
					      B(1)*B(4))*pg2NB0 + \
	  (4*K2*Pi^4*B0^2*B(1) + (120*K1*B(1)^5)/B0^6 - \
	   (480*K1*B(1)^3*B(2))/B0^5 + (360*K1*B(1)*B(2)^2)/B0^4 + \
	   20*K2*Pi^2*B(3) + (360*K1*B(1)^2*B(3))/B0^4 - \
	   (240*K1*B(2)*B(3))/B0^3 - (240*K1*B(1)*B(4))/B0^3 + \
	   60*K2*B(1)^2*pg21 + 120*K2*B0*B(2)*pg21 - 60*B(1)*(B(2)^2 + \
							     B(1)*B(3))*pg3B0 \
	   +  60*B(1)*(B(2)^2 + B(1)*B(3))*pg3NB0 +  5*K2*B0^4*pg41 - \
	   20*B(1)^3*B(2)*pg4B0 + 20*B(1)^3*B(2)*pg4NB0 - B(1)^5*pg5B0 \
	   + B(1)^5*pg5NB0 - 120*B(3)*d1f0 - 60*B(1)^2*d2f0 - \
	   120*B0*B(2)*d2f0 - 60*B0^2*B(1)*d3f0 - \
	   5*B0^4*d4f0)/120)/(-denum);
  
  B(6) = -(-(K2*Pi^6*B0^5)/945 - (K2*Pi^4*B0*B(1)^2)/30 \
	   +(K1*B(1)^6)/B0^7 - (K2*Pi^4*B0^2*B(2))/30 - \
	   (5*K1*B(1)^4*B(2))/B0^6 + (6*K1*B(1)^2*B(2)^2)/B0^5 - \
	   (K1*B(2)^3)/B0^4 + (4*K1*B(1)^3*B(3))/B0^5 - \
	   (6*K1*B(1)*B(2)*B(3))/B0^4 + (K1*B(3)^2)/B0^3 - \
	   (K2*Pi^2*B(4))/6 - (3*K1*B(1)^2*B(4))/B0^4 + \
	   (2*K1*B(2)*B(4))/B0^3 + (2*K1*B(1)*B(5))/B0^3 - \
	   K2*B(1)*B(2)*pg21 - K2*B0*B(3)*pg21 + (B(3)^2/2 + \
						  B(2)*B(4) + \
						  B(1)*B(5))*pg2B0 - \
	   ((B(3)^2 + 2*B(2)*B(4) + 2*B(1)*B(5))*pg2NB0)/2 + \
	   (B(2)^3*pg3B0)/6 + B(1)*B(2)*B(3)*pg3B0 + \
	   (B(1)^2*B(4)*pg3B0)/2 - (B(2)^3*pg3NB0)/ 6 - \
	   B(1)*B(2)*B(3)*pg3NB0 - (B(1)^2*B(4)*pg3NB0)/2 - \
	   (K2*B0^3*B(1)*pg41)/6 + (B(1)^2*B(2)^2*pg4B0)/4 + \
	   (B(1)^3*B(3)*pg4B0)/6 - (B(1)^2*B(2)^2*pg4NB0)/4 - \
	   (B(1)^3*B(3)*pg4NB0)/6 + (B(1)^4*B(2)*pg5B0)/24 - \
	   (B(1)^4*B(2)*pg5NB0)/24 + (B(1)^6*pg6B0)/720 - \
	   (B(1)^6*pg6NB0)/720 + B(4)*d1f0 + B(1)*B(2)*d2f0 + \
	   B0*B(3)*d2f0 + (B0*B(1)^2*d3f0)/2 + (B0^2*B(2)*d3f0)/2 + \
	   (B0^3*B(1)*d4f0)/6 + (B0^5*d5f0)/120)/(-denum);
  
 
  B(7) = ((K2*Pi^6*B0^4*B(1))/189 + (K2*Pi^4*B(1)^3)/90 + \
	  (K1*B(1)^7)/B0^8 + (K2*Pi^4*B0*B(1)*B(2))/15 - \
	  (6*K1*B(1)^5*B(2))/B0^7 + (10*K1*B(1)^3*B(2)^2)/B0^6 - \
	  (4*K1*B(1)*B(2)^3)/B0^5 + (K2*Pi^4*B0^2*B(3))/30 + \
	  (5*K1*B(1)^4*B(3))/B0^6 - (12*K1*B(1)^2*B(2)*B(3))/B0^5 + \
	  (3*K1*B(2)^2*B(3))/B0^4 + (3*K1*B(1)*B(3)^2)/B0^4 - \
	  (4*K1*B(1)^3*B(4))/B0^5 + (6*K1*B(1)*B(2)*B(4))/B0^4 - \
	  (2*K1*B(3)*B(4))/B0^3 + (K2*Pi^2*B(5))/6 + \
	  (3*K1*B(1)^2*B(5))/B0^4 - (2*K1*B(2)*B(5))/B0^3 - \
	  (2*K1*B(1)*B(6))/B0^3 + (K2*B(2)^2*pg21)/2 + \
	  K2*B(1)*B(3)*pg21 + K2*B0*B(4)*pg21 - (B(3)*B(4) + B(2)*B(5) \
						 + B(1)*B(6))*pg2B0 + \
	  (B(3)*B(4) + B(2)*B(5) + B(1)*B(6))*pg2NB0 - \
	  (B(2)^2*B(3)*pg3B0)/2 - (B(1)*B(3)^2*pg3B0)/2 - \
	  B(1)*B(2)*B(4)*pg3B0 - (B(1)^2*B(5)*pg3B0)/2 + \
	  (B(2)^2*B(3)*pg3NB0)/2 + (B(1)*B(3)^2*pg3NB0)/2 + \
	  B(1)*B(2)*B(4)*pg3NB0 + (B(1)^2*B(5)*pg3NB0)/2 + \
	  (K2*B0^2*B(1)^2*pg41)/4 + (K2*B0^3*B(2)*pg41)/6 - \
	  (B(1)*B(2)^3*pg4B0)/6 - (B(1)^2*B(2)*B(3)*pg4B0)/2 - \
	  (B(1)^3*B(4)*pg4B0)/6 + (B(1)*B(2)^3*pg4NB0)/6 + \
	  (B(1)^2*B(2)*B(3)*pg4NB0)/2 + (B(1)^3*B(4)*pg4NB0)/6 - \
	  (B(1)^3*B(2)^2*pg5B0)/12 - (B(1)^4*B(3)*pg5B0)/24 + \
	  (B(1)^3*B(2)^2*pg5NB0)/12 + (B(1)^4*B(3)*pg5NB0)/24 + \
	  (K2*B0^6*pg61)/720 - (B(1)^5*B(2)*pg6B0)/120 + \
	  (B(1)^5*B(2)*pg6NB0)/120 - (B(1)^7*pg7B0)/5040 + \
	  (B(1)^7*pg7NB0)/5040 - B(5)*d1f0 - (B(2)^2*d2f0)/2 - \
	  B(1)*B(3)*d2f0 - B0*B(4)*d2f0 - (B(1)^3*d3f0)/6 - \
	  B0*B(1)*B(2)*d3f0 - (B0^2*B(3)*d3f0)/2 - (B0^2*B(1)^2*d4f0)/4 - \
	  (B0^3*B(2)*d4f0)/6 - (B0^4*B(1)*d5f0)/24 - \
	  (B0^6*d6f0)/720)/(-denum);
  
  
  B(8) = -(-(K2*Pi^8*B0^7)/9450 - (2*K2*Pi^6*B0^3*B(1)^2)/189 + \
	   (K1*B(1)^8)/B0^9 - (K2*Pi^6*B0^4*B(2))/189 - \
	   (K2*Pi^4*B(1)^2*B(2))/30 - (7*K1*B(1)^6*B(2))/B0^8 - \
	   (K2*Pi^4*B0*B(2)^2)/30 + (15*K1*B(1)^4*B(2)^2)/B0^7 - \
	   (10*K1*B(1)^2*B(2)^3)/B0^6 + (K1*B(2)^4)/B0^5 - \
	   (K2*Pi^4*B0*B(1)*B(3))/15 + (6*K1*B(1)^5*B(3))/B0^7 - \
	   (20*K1*B(1)^3*B(2)*B(3))/B0^6 + \
	   (12*K1*B(1)*B(2)^2*B(3))/B0^5 + (6*K1*B(1)^2*B(3)^2)/B0^5 - \
	   (3*K1*B(2)*B(3)^2)/B0^4 - (K2*Pi^4*B0^2*B(4))/30 - \
	   (5*K1*B(1)^4*B(4))/B0^6 + (12*K1*B(1)^2*B(2)*B(4))/B0^5 - \
	   (3*K1*B(2)^2*B(4))/B0^4 - (6*K1*B(1)*B(3)*B(4))/B0^4 + \
	   (K1*B(4)^2)/B0^3 + (4*K1*B(1)^3*B(5))/B0^5 - \
	   (6*K1*B(1)*B(2)*B(5))/B0^4 + (2*K1*B(3)*B(5))/B0^3 - \
	   (K2*Pi^2*B(6))/6 - (3*K1*B(1)^2*B(6))/B0^4 + \
	   (2*K1*B(2)*B(6))/B0^3 + (2*K1*B(1)*B(7))/B0^3 - \
	   K2*B(2)*B(3)*pg21 - K2*B(1)*B(4)*pg21 - K2*B0*B(5)*pg21 + \
	   (B(4)^2/2 + B(3)*B(5) + B(2)*B(6) + B(1)*B(7))*pg2B0 - \
	   ((B(4)^2 + 2*B(3)*B(5) + 2*B(2)*B(6) + \
	     2*B(1)*B(7))*pg2NB0)/2 + (B(2)*B(3)^2*pg3B0)/2 + \
	   (B(2)^2*B(4)*pg3B0)/2 + B(1)*B(3)*B(4)*pg3B0 + \
	   B(1)*B(2)*B(5)*pg3B0 + (B(1)^2*B(6)*pg3B0)/2 - \
	   (B(2)*B(3)^2*pg3NB0)/2 - (B(2)^2*B(4)*pg3NB0)/2 - \
	   B(1)*B(3)*B(4)*pg3NB0 - B(1)*B(2)*B(5)*pg3NB0 - \
	   (B(1)^2*B(6)*pg3NB0)/2 - (K2*B0*B(1)^3*pg41)/6 - \
	   (K2*B0^2*B(1)*B(2)*pg41)/2 - (K2*B0^3*B(3)*pg41)/6 + \
	   (B(2)^4*pg4B0)/24 + (B(1)*B(2)^2*B(3)*pg4B0)/2 + \
	   (B(1)^2*B(3)^2*pg4B0)/4 + (B(1)^2*B(2)*B(4)*pg4B0)/2 + \
	   (B(1)^3*B(5)*pg4B0)/6 - (B(2)^4*pg4NB0)/24 - \
	   (B(1)*B(2)^2*B(3)*pg4NB0)/2 - (B(1)^2*B(3)^2*pg4NB0)/4 - \
	   (B(1)^2*B(2)*B(4)*pg4NB0)/2 - (B(1)^3*B(5)*pg4NB0)/6 + \
	   (B(1)^2*B(2)^3*pg5B0)/12 + (B(1)^3*B(2)*B(3)*pg5B0)/6 + \
	   (B(1)^4*B(4)*pg5B0)/24 - (B(1)^2*B(2)^3*pg5NB0)/12 - \
	   (B(1)^3*B(2)*B(3)*pg5NB0)/6 - (B(1)^4*B(4)*pg5NB0)/24 - \
	   (K2*B0^5*B(1)*pg61)/120 + (B(1)^4*B(2)^2*pg6B0)/48 + \
	   (B(1)^5*B(3)*pg6B0)/120 - (B(1)^4*B(2)^2*pg6NB0)/48 - \
	   (B(1)^5*B(3)*pg6NB0)/120 + (B(1)^6*B(2)*pg7B0)/720 - \
	   (B(1)^6*B(2)*pg7NB0)/720 + (B(1)^8*pg8B0)/40320 - \
	   (B(1)^8*pg8NB0)/40320 + B(6)*d1f0 + B(2)*B(3)*d2f0 + \
	   B(1)*B(4)*d2f0 + B0*B(5)*d2f0 + (B(1)^2*B(2)*d3f0)/2 + \
	   (B0*B(2)^2*d3f0)/2 + B0*B(1)*B(3)*d3f0 + (B0^2*B(4)*d3f0)/2 \
	   + (B0*B(1)^3*d4f0)/6 + (B0^2*B(1)*B(2)*d4f0)/2 + \
	   (B0^3*B(3)*d4f0)/6 + (B0^3*B(1)^2*d5f0)/12 + \
	   (B0^4*B(2)*d5f0)/24 + (B0^5*B(1)*d6f0)/120 + \
	   (B0^7*d7f0)/5040)/(-denum);

 
  B(9) = ((K2*Pi^8*B0^6*B(1))/1350 + (2*K2*Pi^6*B0^2*B(1)^3)/ \
          189 + (K1*B(1)^9)/B0^10 + (4*K2*Pi^6*B0^3*B(1)*B(2))/189 - \
          (8*K1*B(1)^7*B(2))/B0^9 + (K2*Pi^4*B(1)*B(2)^2)/30 + \
          (21*K1*B(1)^5*B(2)^2)/B0^8 - (20*K1*B(1)^3*B(2)^3)/B0^7 + \
          (5*K1*B(1)*B(2)^4)/B0^6 + (K2*Pi^6*B0^4*B(3))/189 + \
          (K2*Pi^4*B(1)^2*B(3))/30 + (7*K1*B(1)^6*B(3))/B0^8 + \
          (K2*Pi^4*B0*B(2)*B(3))/15 - (30*K1*B(1)^4*B(2)*B(3))/B0^7 + \
          (30*K1*B(1)^2*B(2)^2*B(3))/B0^6 - (4*K1*B(2)^3*B(3))/B0^5 + \
          (10*K1*B(1)^3*B(3)^2)/B0^6 - (12*K1*B(1)*B(2)*B(3)^2)/B0^5 + \
          (K1*B(3)^3)/B0^4 + (K2*Pi^4*B0*B(1)*B(4))/15 - \
          (6*K1*B(1)^5*B(4))/B0^7 + (20*K1*B(1)^3*B(2)*B(4))/B0^6 - \
          (12*K1*B(1)*B(2)^2*B(4))/B0^5 - (12*K1*B(1)^2*B(3)*B(4))/B0^5 + \
          (6*K1*B(2)*B(3)*B(4))/B0^4 + (3*K1*B(1)*B(4)^2)/B0^4 + \
          (K2*Pi^4*B0^2*B(5))/30 + (5*K1*B(1)^4*B(5))/B0^6 - \
          (12*K1*B(1)^2*B(2)*B(5))/B0^5 + (3*K1*B(2)^2*B(5))/B0^4 + \
          (6*K1*B(1)*B(3)*B(5))/B0^4 - (2*K1*B(4)*B(5))/B0^3 - \
          (4*K1*B(1)^3*B(6))/B0^5 + (6*K1*B(1)*B(2)*B(6))/B0^4 - \
          (2*K1*B(3)*B(6))/B0^3 + (K2*Pi^2*B(7))/6 + (3*K1*B(1)^2*B(7))/ \
          B0^4 - (2*K1*B(2)*B(7))/B0^3 - (2*K1*B(1)*B(8))/B0^3 + \
          (K2*B(3)^2*pg21)/2 + K2*B(2)*B(4)*pg21 + \
          K2*B(1)*B(5)*pg21 + K2*B0*B(6)*pg21 - \
          (B(4)*B(5) + B(3)*B(6) + B(2)*B(7) + B(1)*B(8))*pg2B0 + \
          (B(4)*B(5) + B(3)*B(6) + B(2)*B(7) + B(1)*B(8))* \
          pg2NB0 - (B(3)^3*pg3B0)/6 - \
          B(2)*B(3)*B(4)*pg3B0 - (B(1)*B(4)^2*pg3B0)/ \
          2 - (B(2)^2*B(5)*pg3B0)/2 - B(1)*B(3)*B(5)* \
          pg3B0 - B(1)*B(2)*B(6)*pg3B0 - \
          (B(1)^2*B(7)*pg3B0)/2 + (B(3)^3*pg3NB0)/ \
          6 + B(2)*B(3)*B(4)*pg3NB0 + \
          (B(1)*B(4)^2*pg3NB0)/2 + \
          (B(2)^2*B(5)*pg3NB0)/2 + B(1)*B(3)*B(5)* \
          pg3NB0 + B(1)*B(2)*B(6)*pg3NB0 + \
          (B(1)^2*B(7)*pg3NB0)/2 + (K2*B(1)^4*pg41)/ \
          24 + (K2*B0*B(1)^2*B(2)*pg41)/2 + \
          (K2*B0^2*B(2)^2*pg41)/4 + \
          (K2*B0^2*B(1)*B(3)*pg41)/2 + \
          (K2*B0^3*B(4)*pg41)/6 - (B(2)^3*B(3)*pg4B0)/ \
          6 - (B(1)*B(2)*B(3)^2*pg4B0)/2 - \
          (B(1)*B(2)^2*B(4)*pg4B0)/2 - \
          (B(1)^2*B(3)*B(4)*pg4B0)/2 - \
          (B(1)^2*B(2)*B(5)*pg4B0)/2 - \
          (B(1)^3*B(6)*pg4B0)/6 + \
          (B(2)^3*B(3)*pg4NB0)/6 + \
          (B(1)*B(2)*B(3)^2*pg4NB0)/2 + \
          (B(1)*B(2)^2*B(4)*pg4NB0)/2 + \
          (B(1)^2*B(3)*B(4)*pg4NB0)/2 + \
          (B(1)^2*B(2)*B(5)*pg4NB0)/2 + \
          (B(1)^3*B(6)*pg4NB0)/6 - \
          (B(1)*B(2)^4*pg5B0)/24 - \
          (B(1)^2*B(2)^2*B(3)*pg5B0)/4 - \
          (B(1)^3*B(3)^2*pg5B0)/12 - \
          (B(1)^3*B(2)*B(4)*pg5B0)/6 - \ 
          (B(1)^4*B(5)*pg5B0)/24 + \
          (B(1)*B(2)^4*pg5NB0)/24 + \
          (B(1)^2*B(2)^2*B(3)*pg5NB0)/4 + \
          (B(1)^3*B(3)^2*pg5NB0)/12 + \
          (B(1)^3*B(2)*B(4)*pg5NB0)/6 + \
          (B(1)^4*B(5)*pg5NB0)/24 + \
          (K2*B0^4*B(1)^2*pg61)/48 + \
          (K2*B0^5*B(2)*pg61)/120 - \
          (B(1)^3*B(2)^3*pg6B0)/36 - \
          (B(1)^4*B(2)*B(3)*pg6B0)/24 - \
          (B(1)^5*B(4)*pg6B0)/120 + \
          (B(1)^3*B(2)^3*pg6NB0)/36 + \
          (B(1)^4*B(2)*B(3)*pg6NB0)/24 + \
          (B(1)^5*B(4)*pg6NB0)/120 - \
          (B(1)^5*B(2)^2*pg7B0)/240 - \
          (B(1)^6*B(3)*pg7B0)/720 + \
          (B(1)^5*B(2)^2*pg7NB0)/240 + \
          (B(1)^6*B(3)*pg7NB0)/720 + \
          (K2*B0^8*polygamma(8, 1])/40320 - (B(1)^7*B(2)*pg8B0)/ \
          5040 + (B(1)^7*B(2)*pg8NB0)/5040 - \
          (B(1)^9*pg9B0)/362880 + (B(1)^9*pg9NB0)/ \
          362880 - B(7)*d1f0 - (B(3)^2*d2f0)/2 - \
          B(2)*B(4)*d2f0 - B(1)*B(5)*d2f0 - \
          B0*B(6)*d2f0 - (B(1)*B(2)^2*d3f0)/2 - \
          (B(1)^2*B(3)*d3f0)/2 - B0*B(2)*B(3)* \
          d3f0 - B0*B(1)*B(4)*d3f0 - \
          (B0^2*B(5)*d3f0)/2 - (B(1)^4*d4f0)/ \
          24 - (B0*B(1)^2*B(2)*d4f0)/2 - \
          (B0^2*B(2)^2*d4f0)/4 - \
          (B0^2*B(1)*B(3)*d4f0)/2 - \
          (B0^3*B(4)*d4f0)/6 - \
          (B0^2*B(1)^3*d5f0)/12 - \ 
          (B0^3*B(1)*B(2)*d5f0)/6 - \
          (B0^4*B(3)*d5f0)/24 - \
          (B0^4*B(1)^2*d6f0)/48 - \
          (B0^5*B(2)*d6f0)/120 - \
          (B0^6*B(1)*d7f0)/720 - (B0^8*d8f0)/ \
          40320)/(-denum);
 
 B(10) = -(-(K2*Pi^10*B0^9)/93555 - (K2*Pi^8*B0^5*B(1)^2)/450 - \
	    (K2*Pi^6*B0*B(1)^4)/189 + (K1*B(1)^10)/B0^11 - \
	    (K2*Pi^8*B0^6*B(2))/1350 - (2*K2*Pi^6*B0^2*B(1)^2*B(2))/63 - \
	    (9*K1*B(1)^8*B(2))/B0^10 - (2*K2*Pi^6*B0^3*B(2)^2)/189 + \
	    (28*K1*B(1)^6*B(2)^2)/B0^9 - (K2*Pi^4*B(2)^3)/90 - \
	    (35*K1*B(1)^4*B(2)^3)/B0^8 + (15*K1*B(1)^2*B(2)^4)/B0^7 - \
	    (K1*B(2)^5)/B0^6 - (4*K2*Pi^6*B0^3*B(1)*B(3))/189 + \
            (8*K1*B(1)^7*B(3))/B0^9 - (K2*Pi^4*B(1)*B(2)*B(3))/15 - \
            (42*K1*B(1)^5*B(2)*B(3))/B0^8 + (60*K1*B(1)^3*B(2)^2*B(3))/ \
            B0^7 - (20*K1*B(1)*B(2)^3*B(3))/B0^6 - (K2*Pi^4*B0*B(3)^2)/ \
            30 + (15*K1*B(1)^4*B(3)^2)/B0^7 - (30*K1*B(1)^2*B(2)*B(3)^2)/ \
            B0^6 + (6*K1*B(2)^2*B(3)^2)/B0^5 + (4*K1*B(1)*B(3)^3)/B0^5 - \
            (K2*Pi^6*B0^4*B(4))/189 - (K2*Pi^4*B(1)^2*B(4))/30 - \
            (7*K1*B(1)^6*B(4))/B0^8 - (K2*Pi^4*B0*B(2)*B(4))/15 + \
            (30*K1*B(1)^4*B(2)*B(4))/B0^7 - (30*K1*B(1)^2*B(2)^2*B(4))/ \
            B0^6 + (4*K1*B(2)^3*B(4))/B0^5 - (20*K1*B(1)^3*B(3)*B(4))/ \
            B0^6 + (24*K1*B(1)*B(2)*B(3)*B(4))/B0^5 - (3*K1*B(3)^2*B(4))/ \
            B0^4 + (6*K1*B(1)^2*B(4)^2)/B0^5 - (3*K1*B(2)*B(4)^2)/B0^4 - \
            (K2*Pi^4*B0*B(1)*B(5))/15 + (6*K1*B(1)^5*B(5))/B0^7 - \
            (20*K1*B(1)^3*B(2)*B(5))/B0^6 + (12*K1*B(1)*B(2)^2*B(5))/B0^5 + \
            (12*K1*B(1)^2*B(3)*B(5))/B0^5 - (6*K1*B(2)*B(3)*B(5))/B0^4 - \
            (6*K1*B(1)*B(4)*B(5))/B0^4 + (K1*B(5)^2)/B0^3 - \
            (K2*Pi^4*B0^2*B(6))/30 - (5*K1*B(1)^4*B(6))/B0^6 + \
            (12*K1*B(1)^2*B(2)*B(6))/B0^5 - (3*K1*B(2)^2*B(6))/B0^4 - \ 
            (6*K1*B(1)*B(3)*B(6))/B0^4 + (2*K1*B(4)*B(6))/B0^3 + \
            (4*K1*B(1)^3*B(7))/B0^5 - (6*K1*B(1)*B(2)*B(7))/B0^4 + \
            (2*K1*B(3)*B(7))/B0^3 - (K2*Pi^2*B(8))/6 - (3*K1*B(1)^2*B(8))/ \
            B0^4 + (2*K1*B(2)*B(8))/B0^3 + (2*K1*B(1)*B(9))/B0^3 - \
            K2*B(3)*B(4)*pg21 - K2*B(2)*B(5)*pg21 - \
            K2*B(1)*B(6)*pg21 - K2*B0*B(7)*pg21 + \
            (B(5)^2/2 + B(4)*B(6) + B(3)*B(7) + B(2)*B(8) + B(1)*B(9))* \
            pg2B0 - ((B(5)^2 + 2*(B(4)*B(6) + B(3)*B(7) + \
				  B(2)*B(8) + B(1)*B(9)))*pg2NB0)/2 + \
            (B(3)^2*B(4)*pg3B0)/2 + \
            (B(2)*B(4)^2*pg3B0)/2 + B(2)*B(3)*B(5)* \
            pg3B0 + B(1)*B(4)*B(5)*pg3B0 + \
            (B(2)^2*B(6)*pg3B0)/2 + B(1)*B(3)*B(6)* \
            pg3B0 + B(1)*B(2)*B(7)*pg3B0 + \
            (B(1)^2*B(8)*pg3B0)/2 - \
            (B(3)^2*B(4)*pg3NB0)/2 - \
            (B(2)*B(4)^2*pg3NB0)/2 - B(2)*B(3)*B(5)* \
            pg3NB0 - B(1)*B(4)*B(5)*pg3NB0 - \
            (B(2)^2*B(6)*pg3NB0)/2 - B(1)*B(3)*B(6)*\ 
            pg3NB0 - B(1)*B(2)*B(7)*pg3NB0 - \
            (B(1)^2*B(8)*pg3NB0)/2 - \
            (K2*B(1)^3*B(2)*pg41)/6 - (K2*B0*B(1)*B(2)^2* \
				       pg41)/2 - (K2*B0*B(1)^2*B(3)*pg41)/2 - \
            (K2*B0^2*B(2)*B(3)*pg41)/2 - \
            (K2*B0^2*B(1)*B(4)*pg41)/2 - \
            (K2*B0^3*B(5)*pg41)/6 + \
            (B(2)^2*B(3)^2*pg4B0)/4 + \
            (B(1)*B(3)^3*pg4B0)/6 + \
            (B(2)^3*B(4)*pg4B0)/6 + B(1)*B(2)*B(3)*B(4)* \
            pg4B0 + (B(1)^2*B(4)^2*pg4B0)/4 + \
            (B(1)*B(2)^2*B(5)*pg4B0)/2 + \
            (B(1)^2*B(3)*B(5)*pg4B0)/2 + \
            (B(1)^2*B(2)*B(6)*pg4B0)/2 + \
            (B(1)^3*B(7)*pg4B0)/6 - \
            (B(2)^2*B(3)^2*pg4NB0)/4 - \
            (B(1)*B(3)^3*pg4NB0)/6 - \
            (B(2)^3*B(4)*pg4NB0)/6 - B(1)*B(2)*B(3)*B(4)* \
            pg4NB0 - (B(1)^2*B(4)^2*pg4NB0)/4 - \
            (B(1)*B(2)^2*B(5)*pg4NB0)/2 - \
            (B(1)^2*B(3)*B(5)*pg4NB0)/2 - \
            (B(1)^2*B(2)*B(6)*pg4NB0)/2 - \
            (B(1)^3*B(7)*pg4NB0)/6 + (B(2)^5*pg5B0)/ \
            120 + (B(1)*B(2)^3*B(3)*pg5B0)/6 + \
            (B(1)^2*B(2)*B(3)^2*pg5B0)/4 + \
            (B(1)^2*B(2)^2*B(4)*pg5B0)/4 + \
            (B(1)^3*B(3)*B(4)*pg5B0)/6 + \
            (B(1)^3*B(2)*B(5)*pg5B0)/6 + \
            (B(1)^4*B(6)*pg5B0)/24 - \
            (B(2)^5*pg5NB0)/120 - \
            (B(1)*B(2)^3*B(3)*pg5NB0)/6 - \
            (B(1)^2*B(2)*B(3)^2*pg5NB0)/4 - \
            (B(1)^2*B(2)^2*B(4)*pg5NB0)/4 - \
            (B(1)^3*B(3)*B(4)*pg5NB0)/6 - \
            (B(1)^3*B(2)*B(5)*pg5NB0)/6 - \
            (B(1)^4*B(6)*pg5NB0)/24 - \
            (K2*B0^3*B(1)^3*pg61)/36 - \
            (K2*B0^4*B(1)*B(2)*pg61)/24 - \
            (K2*B0^5*B(3)*pg61)/120 + \
            (B(1)^2*B(2)^4*pg6B0)/48 + \
            (B(1)^3*B(2)^2*B(3)*pg6B0)/12 + \
            (B(1)^4*B(3)^2*pg6B0)/48 + \
            (B(1)^4*B(2)*B(4)*pg6B0)/24 + \
            (B(1)^5*B(5)*pg6B0)/120 - \
            (B(1)^2*B(2)^4*pg6NB0)/48 - \
            (B(1)^3*B(2)^2*B(3)*pg6NB0)/12 - \
            (B(1)^4*B(3)^2*pg6NB0)/48 - \
            (B(1)^4*B(2)*B(4)*pg6NB0)/24 - \
            (B(1)^5*B(5)*pg6NB0)/120 + \
            (B(1)^4*B(2)^3*pg7B0)/144 + \
            (B(1)^5*B(2)*B(3)*pg7B0)/120 + \
            (B(1)^6*B(4)*pg7B0)/720 - \
            (B(1)^4*B(2)^3*pg7NB0)/144 - \
            (B(1)^5*B(2)*B(3)*pg7NB0)/120 - \
            (B(1)^6*B(4)*pg7NB0)/720 - \
            (K2*B0^7*B(1)*polygamma(8, 1])/5040 + \
            (B(1)^6*B(2)^2*pg8B0)/1440 + \
            (B(1)^7*B(3)*pg8B0)/5040 - \
            (B(1)^6*B(2)^2*pg8NB0)/1440 - \
            (B(1)^7*B(3)*pg8NB0)/5040 + \
            (B(1)^8*B(2)*pg9B0)/40320 - \
            (B(1)^8*B(2)*pg9NB0)/40320 + \
            (B(1)^10*pg10B0)/3628800 - \
            (B(1)^10*pg10NB0)/3628800 + \
            B(8)*d1f0 + B(3)*B(4)*d2f0 + \
            B(2)*B(5)*d2f0 + B(1)*B(6)*d2f0 + \
            B0*B(7)*d2f0 + (B(2)^3*d3f0)/6 + \
            B(1)*B(2)*B(3)*d3f0 + \
            (B0*B(3)^2*d3f0)/2 + \
            (B(1)^2*B(4)*d3f0)/2 + B0*B(2)*B(4)* \
            d3f0 + B0*B(1)*B(5)*d3f0 + \
            (B0^2*B(6)*d3f0)/2 + \
            (B(1)^3*B(2)*d4f0)/6 + \
            (B0*B(1)*B(2)^2*d4f0)/2 + \
            (B0*B(1)^2*B(3)*d4f0)/2 + \
            (B0^2*B(2)*B(3)*d4f0)/2 + \
            (B0^2*B(1)*B(4)*d4f0)/2 + \
            (B0^3*B(5)*d4f0)/6 + \
            (B0*B(1)^4*d5f0)/24 + \
            (B0^2*B(1)^2*B(2)*d5f0)/4 + \
            (B0^3*B(2)^2*d5f0)/12 + \
            (B0^3*B(1)*B(3)*d5f0)/6 + \
            (B0^4*B(4)*d5f0)/24 + \
           (B0^3*B(1)^3*d6f0)/36 + \
           (B0^4*B(1)*B(2)*d6f0)/24 + \
           (B0^5*B(3)*d6f0)/120 + \
           (B0^5*B(1)^2*d7f0)/240 + \
           (B0^6*B(2)*d7f0)/720 + \
           (B0^7*B(1)*d8f0)/5040 + \
           (B0^9*d9f0)/362880)/(-denum);
