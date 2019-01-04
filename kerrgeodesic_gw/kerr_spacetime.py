r"""
Kerr black hole

REFERENCES:

- \J. M. Bardeen, W. H. Press and S. A. Teukolsky, Astrophys. J. **178**,
  347 (1972), :doi:`10.1086/151796`
- \L. Dai and R. Blandford, Mon. Not. Roy. Astron. Soc. **434**, 2948 (2013),
  :doi:`10.1093/mnras/stt1209`

"""
#******************************************************************************
#       Copyright (C) 2018 Eric Gourgoulhon <eric.gourgoulhon@obspm.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.functions.trig import cos, sin, acos
from sage.functions.other import sqrt
from sage.rings.rational_field import QQ
from sage.symbolic.constants import pi
from sage.misc.cachefunc import cached_method
from sage.manifolds.differentiable.pseudo_riemannian import PseudoRiemannianManifold

class KerrBH(PseudoRiemannianManifold):
    r"""
    Spacetime representing the Kerr black hole.

    The Kerr spacetime is generated as a 4-dimensional Lorentzian manifold,
    endowed with the Boyer-Lindquist coordinates (default chart).

    INPUT:

    - ``a`` -- reduced angular momentum
    - ``m`` -- (default: ``1``) total mass
    - ``manifold_name`` -- (default: ``'M'``) string; name (symbol) given to
      the spacetime manifold
    - ``manifold_latex_name`` -- (default: ``None``) string; LaTeX symbol to
      denote the spacetime manifold; if none is provided, it is set to
      ``manifold_name``
    - ``metric_name`` -- (default: ``'g'``) string; name (symbol) given to the
      metric tensor
    - ``metric_latex_name`` -- (default: ``None``) string; LaTeX symbol to
      denote the metric tensor; if none is provided, it is set to
      ``metric_name``

    EXAMPLES:

    Creating a Kerr spacetime with symbolic parameters `(a, m)`::

        sage: from kerrgeodesic_gw import KerrBH
        sage: a, m = var('a m')
        sage: BH = KerrBH(a, m); BH
        4-dimensional Lorentzian manifold M
        sage: dim(BH)
        4

    The Boyer-Lindquist chart::

        sage: BH.BoyerLindquist_coordinates()
        Chart (M, (t, r, th, ph))
        sage: latex(_)
        \left(M,(t, r, {\theta}, {\phi})\right)

    The Kerr metric::

        sage: g = BH.metric(); g
        Lorentzian metric g on the 4-dimensional Lorentzian manifold M
        sage: g.display()
        g = -(a^2*cos(th)^2 - 2*m*r + r^2)/(a^2*cos(th)^2 + r^2) dt*dt
         - 2*a*m*r*sin(th)^2/(a^2*cos(th)^2 + r^2) dt*dph
         + (a^2*cos(th)^2 + r^2)/(a^2 - 2*m*r + r^2) dr*dr
         + (a^2*cos(th)^2 + r^2) dth*dth
         - 2*a*m*r*sin(th)^2/(a^2*cos(th)^2 + r^2) dph*dt
         + (2*a^2*m*r*sin(th)^4 + (a^2*r^2 + r^4 + (a^4 + a^2*r^2)*cos(th)^2)*sin(th)^2)/(a^2*cos(th)^2 + r^2) dph*dph
        sage: g[0,3]
        -2*a*m*r*sin(th)^2/(a^2*cos(th)^2 + r^2)

    A Kerr spacetime with specific numerical values for `(a,m)`, namely `m=1`
    and `a=0.9`::

        sage: BH = KerrBH(0.9); BH
        4-dimensional Lorentzian manifold M
        sage: g = BH.metric()
        sage: g.display()  # tol 1.0e-13
        g = -(r^2 + 0.81*cos(th)^2 - 2*r)/(r^2 + 0.81*cos(th)^2) dt*dt
          - 1.8*r*sin(th)^2/(r^2 + 0.81*cos(th)^2) dt*dph
          + (1.0*r^2 + 0.81*cos(th)^2)/(1.0*r^2 - 2.0*r + 0.81) dr*dr
          + (r^2 + 0.81*cos(th)^2) dth*dth
         - 1.8*r*sin(th)^2/(r^2 + 0.81*cos(th)^2) dph*dt
         + (1.62*r*sin(th)^4 + (1.0*r^4 + (0.81*r^2 + 0.6561)*cos(th)^2
            + 0.81*r^2)*sin(th)^2)/(1.0*r^2 + 0.81*cos(th)^2) dph*dph
        sage: g[0,3]
        -1.8*r*sin(th)^2/(r^2 + 0.81*cos(th)^2)

    The Schwarrzschild spacetime as the special case `a=0` of Kerr
    spacetime::

        sage: BH = KerrBH(0, m)
        sage: g = BH.metric()
        sage: g.display()
        g = (2*m - r)/r dt*dt - r/(2*m - r) dr*dr + r^2 dth*dth + r^2*sin(th)^2 dph*dph

    The object returned by :meth:`metric` belongs to the SageMath class
    `PseudoRiemannianMetric <http://doc.sagemath.org/html/en/reference/manifolds/sage/manifolds/differentiable/metric.html>`_,
    for which many methods are available, like ``christoffel_symbols_display()``
    to get the Christoffel symbols with respect to the Boyer-Lindquist
    coordinates (by default, only nonzero and non-redundant symbols are
    displayed)::

        sage: g.christoffel_symbols_display()
        Gam^t_t,r = -m/(2*m*r - r^2)
        Gam^r_t,t = -(2*m^2 - m*r)/r^3
        Gam^r_r,r = m/(2*m*r - r^2)
        Gam^r_th,th = 2*m - r
        Gam^r_ph,ph = (2*m - r)*sin(th)^2
        Gam^th_r,th = 1/r
        Gam^th_ph,ph = -cos(th)*sin(th)
        Gam^ph_r,ph = 1/r
        Gam^ph_th,ph = cos(th)/sin(th)

    or ``ricci()`` to compute the Ricci tensor (identically zero here since we
    are dealing with a solution of Einstein equation in vacuum)::

        sage: g.ricci()
        Field of symmetric bilinear forms Ric(g) on the 4-dimensional
         Lorentzian manifold M
        sage: g.ricci().display()
        Ric(g) = 0

    Various methods of ``KerrBH`` class implement the computations of
    remarkable radii in the Kerr spacetime. Let us use them to reproduce Fig. 1
    of the seminal article by Bardeen, Press and Teukolsky, ApJ **178**, 347
    (1972), :doi:`10.1086/151796`, which displays these radii as functions of
    the black hole spin paramater `a`. The radii of event horizon and inner
    (Cauchy) horizon are obtained by the methods :meth:`event_horizon_radius`
    and :meth:`cauchy_horizon_radius` respectively::

        sage: graph = plot(lambda a: KerrBH(a).event_horizon_radius(),
        ....:              (0., 1.), color='black', thickness=1.5,
        ....:              legend_label=r"$r_{\rm H}$ (event horizon)",
        ....:              axes_labels=[r"$a/M$", r"$r/M$"],
        ....:              gridlines=True, frame=True, axes=False)
        sage: graph += plot(lambda a: KerrBH(a).cauchy_horizon_radius(),
        ....:               (0., 1.), color='black', linestyle=':', thickness=1.5,
        ....:               legend_label=r"$r_{\rm C}$ (Cauchy horizon)")

    The ISCO radius is computed by the method :meth:`isco_radius`::

        sage: graph += plot(lambda a: KerrBH(a).isco_radius(),
        ....:               (0., 1.), thickness=1.5,
        ....:               legend_label=r"$r_{\rm ISCO}$ (prograde)")
        sage: graph += plot(lambda a: KerrBH(a).isco_radius(retrograde=True),
        ....:               (0., 1.), linestyle='--', thickness=1.5,
        ....:               legend_label=r"$r_{\rm ISCO}$ (retrograde)")

    The radius of the marginally bound circular orbit is computed by the method
    :meth:`marginally_bound_orbit_radius`::

        sage: graph += plot(lambda a: KerrBH(a).marginally_bound_orbit_radius(),
        ....:               (0., 1.), color='purple', linestyle='-', thickness=1.5,
        ....:               legend_label=r"$r_{\rm mb}$ (prograde)")
        sage: graph += plot(lambda a: KerrBH(a).marginally_bound_orbit_radius(retrograde=True),
        ....:               (0., 1.), color='purple', linestyle='--', thickness=1.5,
        ....:               legend_label=r"$r_{\rm mb}$ (retrograde)")

    The radius of the photon circular orbit is computed by the method
    :meth:`photon_orbit_radius`::

        sage: graph += plot(lambda a: KerrBH(a).photon_orbit_radius(),
        ....:               (0., 1.), color='gold', linestyle='-', thickness=1.5,
        ....:               legend_label=r"$r_{\rm ph}$ (prograde)")
        sage: graph += plot(lambda a: KerrBH(a).photon_orbit_radius(retrograde=True),
        ....:               (0., 1.), color='gold', linestyle='--', thickness=1.5,
        ....:               legend_label=r"$r_{\rm ph}$ (retrograde)")

    The final plot::

        sage: graph
        Graphics object consisting of 8 graphics primitives

    .. PLOT::

        from kerrgeodesic_gw import KerrBH
        graph = plot(lambda a: KerrBH(a).event_horizon_radius(), \
                     (0., 1.), color='black', thickness=1.5, \
                     legend_label=r"$r_{\rm H}$ (event horizon)", \
                     axes_labels=[r"$a/M$", r"$r/M$"], \
                     gridlines=True, frame=True, axes=False, ymax=10)
        graph += plot(lambda a: KerrBH(a).cauchy_horizon_radius(), \
                      (0., 1.), color='black', linestyle=':', thickness=1.5, \
                      legend_label=r"$r_{\rm C}$ (Cauchy horizon)")
        graph += plot(lambda a: KerrBH(a).isco_radius(), \
                      (0., 1.), thickness=1.5, \
                      legend_label=r"$r_{\rm ISCO}$ (prograde)")
        graph += plot(lambda a: KerrBH(a).isco_radius(retrograde=True), \
                      (0., 1.), linestyle='--', thickness=1.5, \
                      legend_label=r"$r_{\rm ISCO}$ (retrograde)")
        graph += plot(lambda a: KerrBH(a).marginally_bound_orbit_radius(), \
                      (0., 1.), color='purple', linestyle='-', thickness=1.5, \
                      legend_label=r"$r_{\rm mb}$ (prograde)")
        graph += plot(lambda a: KerrBH(a).marginally_bound_orbit_radius(retrograde=True), \
                      (0., 1.), color='purple', linestyle='--', thickness=1.5, \
                      legend_label=r"$r_{\rm mb}$ (retrograde)")
        graph += plot(lambda a: KerrBH(a).photon_orbit_radius(), \
                      (0., 1.), color='gold', linestyle='-', thickness=1.5, \
                      legend_label=r"$r_{\rm ph}$ (prograde)")
        graph += plot(lambda a: KerrBH(a).photon_orbit_radius(retrograde=True), \
                      (0., 1.), color='gold', linestyle='--', thickness=1.5, \
                      legend_label=r"$r_{\rm ph}$ (retrograde)")
        sphinx_plot(graph)

    """
    def __init__(self, a, m=1, manifold_name='M', manifold_latex_name=None,
                 metric_name='g', metric_latex_name=None):
        # Parameters
        self._m = m
        self._a = a
        # Manifold
        PseudoRiemannianManifold.__init__(self, 4, manifold_name,
                                          metric_name=metric_name, signature=2,
                                          latex_name=manifold_latex_name,
                                          metric_latex_name=metric_latex_name)
        # Coordinate charts (not initialized yet)
        self._BLcoord = None # Boyer-Lindquist

    def mass(self):
        r"""
        Return the (ADM) mass of the black hole.

        EXAMPLES::

            sage: from kerrgeodesic_gw import KerrBH
            sage: a, m = var('a m')
            sage: BH = KerrBH(a, m)
            sage: BH.mass()
            m
            sage: KerrBH(a).mass()
            1

        """
        return self._m

    def spin(self):
        r"""
        Return the reduced angular momentum of the black hole.

        EXAMPLES::

            sage: from kerrgeodesic_gw import KerrBH
            sage: a, m = var('a m')
            sage: BH = KerrBH(a, m)
            sage: BH.spin()
            a

        An alias is ``angular_momentum()``::

            sage: BH.angular_momentum()
            a

        """
        return self._a

    angular_momentum = spin

    def BoyerLindquist_coordinates(self, symbols=None, names=None):
        r"""
        Return the chart of Boyer-Lindquist coordinates

        INPUT:

        - ``symbols`` -- (default: ``None``) string defining the coordinate
          text symbols and LaTeX symbols, with the same conventions as the
          argument ``coordinates`` in
          :class:`~sage.manifolds.differentiable.chart.RealDiffChart`; this is
          used only if the Boyer-Lindquist chart has not been already defined;
          if ``None`` the symbols are generated as `(t,r,\theta,\phi)`.
        - ``names`` -- (default: ``None``) unused argument, except if
          ``symbols`` is not provided; it must be a tuple containing
          the coordinate symbols (this is guaranteed if the shortcut operator
          ``<,>`` is used)

        OUTPUT:

        - the chart of Boyer-Lindquist coordinates, as an instance of
          :class:`~sage.manifolds.differentiable.chart.RealDiffChart`

        EXAMPLES::

            sage: from kerrgeodesic_gw import KerrBH
            sage: a, m = var('a m')
            sage: BH = KerrBH(a, m)
            sage: BH.BoyerLindquist_coordinates()
            Chart (M, (t, r, th, ph))
            sage: latex(BH.BoyerLindquist_coordinates())
            \left(M,(t, r, {\theta}, {\phi})\right)

        The coordinate variables are returned by the square bracket operator::

            sage: BH.BoyerLindquist_coordinates()[0]
            t
            sage: BH.BoyerLindquist_coordinates()[1]
            r
            sage: BH.BoyerLindquist_coordinates()[:]
            (t, r, th, ph)

        They can also be obtained via the operator ``<,>`` at the same
        time as the chart itself::

            sage: BLchart.<t, r, th, ph> = BH.BoyerLindquist_coordinates()
            sage: BLchart
            Chart (M, (t, r, th, ph))
            sage: type(ph)
            <type 'sage.symbolic.expression.Expression'>

        Actually, ``BLchart.<t, r, th, ph> = BH.BoyerLindquist_coordinates()``
        is a shortcut for::

            sage: BLchart = BH.BoyerLindquist_coordinates()
            sage: t, r, th, ph = BLchart[:]

        The coordinate symbols can be customized::

            sage: BH = KerrBH(a)
            sage: BH.BoyerLindquist_coordinates(symbols=r"T R Th:\Theta Ph:\Phi")
            Chart (M, (T, R, Th, Ph))
            sage: latex(BH.BoyerLindquist_coordinates())
            \left(M,(T, R, {\Theta}, {\Phi})\right)

        """
        if self._BLcoord is None:
            if symbols is None:
                if names is None:
                    symbols = 't r th:\\theta ph:\\phi'
                else:
                    names = list(names)
                    if names[2] in ['th', 'theta']:
                        names[2] = names[2] + ':\\theta'
                    if names[3] in ['p', 'ph', 'phi']:
                        names[3] = names[3] + ':\\phi'
                    symbols = (names[0] + ' ' + names[1] + ' ' + names[2] + ' '
                               + names[3])
            coords = symbols.split()  # list of strings, one per coordinate
            # Adding the coordinate ranges:
            coordinates = (coords[0] + ' ' + coords[1] + ' ' + coords[2]
                           + ':(0,pi) ' + coords[3] + ':(0,2*pi)')
            self._BLcoord = self.chart(coordinates=coordinates)
        return self._BLcoord

    def metric(self):
        r"""
        Return the metric tensor.

        EXAMPLES::

            sage: from kerrgeodesic_gw import KerrBH
            sage: a, m = var('a m')
            sage: BH = KerrBH(a, m)
            sage: BH.metric()
            Lorentzian metric g on the 4-dimensional Lorentzian manifold M
            sage: BH.metric().display()
            g = -(a^2*cos(th)^2 - 2*m*r + r^2)/(a^2*cos(th)^2 + r^2) dt*dt
             - 2*a*m*r*sin(th)^2/(a^2*cos(th)^2 + r^2) dt*dph
             + (a^2*cos(th)^2 + r^2)/(a^2 - 2*m*r + r^2) dr*dr
             + (a^2*cos(th)^2 + r^2) dth*dth
             - 2*a*m*r*sin(th)^2/(a^2*cos(th)^2 + r^2) dph*dt
             + (2*a^2*m*r*sin(th)^4 + (a^2*r^2 + r^4 + (a^4 + a^2*r^2)*cos(th)^2)*sin(th)^2)/(a^2*cos(th)^2 + r^2) dph*dph

        The Schwarzschild metric::

            sage: KerrBH(0, m).metric().display()
            g = (2*m - r)/r dt*dt - r/(2*m - r) dr*dr + r^2 dth*dth
             + r^2*sin(th)^2 dph*dph

        """
        if self._metric is None:
            # Initialization of the metric tensor in Boyer-Lindquist coordinates
            cBL = self.BoyerLindquist_coordinates()
            t, r, th, ph = cBL[:]
            g = super(KerrBH, self).metric() # the initialized metric object
            m = self._m
            a = self._a
            r2 = r**2
            a2 = a**2
            rho2 = r2 + (a*cos(th))**2
            Delta = r2 - 2*m*r + a2
            fBL = cBL.frame()  # vector frame associated to BL coordinates
            g[fBL,0,0,cBL] = -1 + 2*m*r/rho2
            g[fBL,0,3,cBL] = -2*a*m*r*sin(th)**2/rho2
            g[fBL,1,1,cBL] = rho2/Delta
            g[fBL,2,2,cBL] = rho2
            g[fBL,3,3,cBL] = (r2 + a2 + 2*m*r*(a*sin(th))**2/rho2)*sin(th)**2
            for i in self.irange():
                g[fBL,i,i,cBL].simplify()
            g[fBL,0,3,cBL].simplify()
        return self._metric


    @cached_method
    def outer_horizon_radius(self):
        r"""
        Return the value of the Boyer-Lindquist coordinate `r` at the black
        hole event horizon.

        EXAMPLES::

            sage: from kerrgeodesic_gw import KerrBH
            sage: a, m = var('a m')
            sage: BH = KerrBH(a, m)
            sage: BH.outer_horizon_radius()
            m + sqrt(-a^2 + m^2)

        An alias is ``event_horizon_radius()``::

            sage: BH.event_horizon_radius()
            m + sqrt(-a^2 + m^2)

        The horizon radius of the Schwarzschild black hole::

            sage: assume(m>0)
            sage: KerrBH(0, m).event_horizon_radius()
            2*m

        The horizon radius of the extreme Kerr black hole (`a=m`)::

            sage: KerrBH(m, m).event_horizon_radius()
            m

        """
        m = self._m
        a = self._a
        return m + sqrt(m**2 - a**2)

    event_horizon_radius = outer_horizon_radius

    @cached_method
    def inner_horizon_radius(self):
        r"""
        Return the value of the Boyer-Lindquist coordinate `r` at the inner
        horizon (Cauchy horizon).

        EXAMPLES::

            sage: from kerrgeodesic_gw import KerrBH
            sage: a, m = var('a m')
            sage: BH = KerrBH(a, m)
            sage: BH.inner_horizon_radius()
            m - sqrt(-a^2 + m^2)

        An alias is ``cauchy_horizon_radius()``::

            sage: BH.cauchy_horizon_radius()
            m - sqrt(-a^2 + m^2)

        """
        m = self._m
        a = self._a
        return m - sqrt(m**2 - a**2)

    cauchy_horizon_radius = inner_horizon_radius

    @cached_method
    def photon_orbit_radius(self, retrograde=False):
        r"""
        Return the Boyer-Lindquist radial coordinate of the circular orbit
        of photons in the equatorial plane.

        INPUT:

        - ``retrograde`` -- (default: ``False``) boolean determining whether
          retrograde or prograde (direct) orbits are considered

        OUTPUT:

        - Boyer-Lindquist radial coordinate `r` of the circular orbit of
          photons in the equatorial plane

        EXAMPLES::

            sage: from kerrgeodesic_gw import KerrBH
            sage: a, m = var('a m')
            sage: BH = KerrBH(a, m)
            sage: BH.photon_orbit_radius()
            2*m*(cos(2/3*arccos(-a/m)) + 1)
            sage: BH.photon_orbit_radius(retrograde=True)
            2*m*(cos(2/3*arccos(a/m)) + 1)

        Photon orbit in Schwarzschild spacetime::

            sage: KerrBH(0, m).photon_orbit_radius()
            3*m

        Photon orbits in extreme Kerr spacetime (`a=m`)::

            sage: KerrBH(m, m).photon_orbit_radius()
            m
            sage: KerrBH(m, m).photon_orbit_radius(retrograde=True)
            4*m

        """
        m = self._m
        a = self._a
        eps = -1 if not retrograde else 1
        # Eq. (2.18) in Bardeen, Press & Teukolsky, ApJ 178, 347 (1972)
        return 2*m*(1 + cos(2*acos(eps*a/m)/3))

    @cached_method
    def marginally_bound_orbit_radius(self, retrograde=False):
        r"""
        Return the Boyer-Lindquist radial coordinate of the marginally bound
        circular orbit in the equatorial plane.

        INPUT:

        - ``retrograde`` -- (default: ``False``) boolean determining whether
          retrograde or prograde (direct) orbits are considered

        OUTPUT:

        - Boyer-Lindquist radial coordinate `r` of the marginally bound
          circular orbit in the equatorial plane

        EXAMPLES::

            sage: from kerrgeodesic_gw import KerrBH
            sage: a, m = var('a m')
            sage: BH = KerrBH(a, m)
            sage: BH.marginally_bound_orbit_radius()
            -a + 2*sqrt(-a + m)*sqrt(m) + 2*m
            sage: BH.marginally_bound_orbit_radius(retrograde=True)
            a + 2*sqrt(a + m)*sqrt(m) + 2*m

        Marginally bound orbit in Schwarzschild spacetime::

            sage: KerrBH(0, m).marginally_bound_orbit_radius()
            4*m

        Marginally bound orbits in extreme Kerr spacetime (`a=m`)::

            sage: KerrBH(m, m).marginally_bound_orbit_radius()
            m
            sage: KerrBH(m, m).marginally_bound_orbit_radius(retrograde=True)
            2*sqrt(2)*m + 3*m

        """
        m = self._m
        a = self._a
        eps = -1 if not retrograde else 1
        # Eq. (2.19) in Bardeen, Press & Teukolsky, ApJ 178, 347 (1972)
        return 2*m + eps*a +2*sqrt(m)*sqrt(m + eps*a)


    @cached_method
    def isco_radius(self, retrograde=False):
        r"""
        Return the Boyer-Lindquist radial coordinate of the innermost stable
        circular orbit (ISCO) in the equatorial plane.

        INPUT:

        - ``retrograde`` -- (default: ``False``) boolean determining whether
          retrograde or prograde (direct) orbits are considered

        OUTPUT:

        - Boyer-Lindquist radial coordinate `r` of the innermost stable
          circular orbit in the equatorial plane

        EXAMPLES::

            sage: from kerrgeodesic_gw import KerrBH
            sage: a, m = var('a m')
            sage: BH = KerrBH(a, m)
            sage: BH.isco_radius()
            m*(sqrt((((a/m + 1)^(1/3) + (-a/m + 1)^(1/3))*(-a^2/m^2 + 1)^(1/3) + 1)^2
             + 3*a^2/m^2) - sqrt(-(((a/m + 1)^(1/3) + (-a/m + 1)^(1/3))*(-a^2/m^2 + 1)^(1/3)
             + 2*sqrt((((a/m + 1)^(1/3) + (-a/m + 1)^(1/3))*(-a^2/m^2 + 1)^(1/3) + 1)^2
             + 3*a^2/m^2) + 4)*(((a/m + 1)^(1/3) + (-a/m + 1)^(1/3))*(-a^2/m^2 + 1)^(1/3) - 2)) + 3)
            sage: BH.isco_radius(retrograde=True)
            m*(sqrt((((a/m + 1)^(1/3) + (-a/m + 1)^(1/3))*(-a^2/m^2 + 1)^(1/3) + 1)^2
             + 3*a^2/m^2) + sqrt(-(((a/m + 1)^(1/3) + (-a/m + 1)^(1/3))*(-a^2/m^2 + 1)^(1/3)
             + 2*sqrt((((a/m + 1)^(1/3) + (-a/m + 1)^(1/3))*(-a^2/m^2 + 1)^(1/3) + 1)^2
             + 3*a^2/m^2) + 4)*(((a/m + 1)^(1/3) + (-a/m + 1)^(1/3))*(-a^2/m^2 + 1)^(1/3) - 2)) + 3)
            sage: KerrBH(0.5).isco_radius()  # tol 1.0e-13
            4.23300252953083
            sage: KerrBH(0.9).isco_radius()  # tol 1.0e-13
            2.32088304176189
            sage: KerrBH(0.98).isco_radius()  # tol 1.0e-13
            1.61402966763547

        ISCO in Schwarzschild spacetime::

            sage: KerrBH(0, m).isco_radius()
            6*m

        ISCO in extreme Kerr spacetime (`a=m`)::

            sage: KerrBH(m, m).isco_radius()
            m
            sage: KerrBH(m, m).isco_radius(retrograde=True)
            9*m

        """
        m = self._m
        a = self._a
        eps = -1 if not retrograde else 1
        # Eq. (2.21) in Bardeen, Press & Teukolsky, ApJ 178, 347 (1972)
        asm = a/m
        asm2 = asm**2
        one_third = QQ(1)/QQ(3)
        z1 = 1 + (1 - asm2)**one_third * ((1 + asm)**one_third
                                          + (1 - asm)**one_third)
        z2 = sqrt(3*asm2 + z1**2)
        return m*(3 + z2 + eps*sqrt((3 - z1)*(3 + z1 + 2*z2)))

    def orbital_angular_velocity(self, r, retrograde=False):
        r"""
        Return the angular velocity on a circular orbit.

        The angular velocity `\Omega` on a circular orbit of Boyer-Lindquist
        radial coordinate `r` around a Kerr black hole of parameters `(m, a)`
        is given by the formula

        .. MATH::
           :label: Omega

            \Omega := \frac{\mathrm{d}\phi}{\mathrm{d}t}
                    = \pm \frac{m^{1/2}}{r^{3/2} \pm a m^{1/2}}

        where `(t,\phi)` are the Boyer-Lindquist time and azimuthal coordinates
        and `\pm` is `+` (resp. `-`) for a prograde (resp. retrograde) orbit.

        INPUT:

        - ``r`` -- Boyer-Lindquist radial coordinate `r` of the circular orbit
        - ``retrograde`` -- (default: ``False``) boolean determining whether
          the orbit is retrograde or prograde

        OUTPUT:

        - Angular velocity `\Omega` computed according to Eq. :eq:`Omega`

        EXAMPLES::

            sage: from kerrgeodesic_gw import KerrBH
            sage: a, m, r = var('a m r')
            sage: BH = KerrBH(a, m)
            sage: BH.orbital_angular_velocity(r)
            sqrt(m)/(a*sqrt(m) + r^(3/2))
            sage: BH.orbital_angular_velocity(r, retrograde=True)
            sqrt(m)/(a*sqrt(m) - r^(3/2))
            sage: KerrBH(0.9).orbital_angular_velocity(4.)  # tol 1.0e-13
            0.112359550561798

        Orbital angular velocity around a Schwarzschild black hole::

            sage: KerrBH(0, m).orbital_angular_velocity(r)
            sqrt(m)/r^(3/2)

        Orbital angular velocity on the prograde ISCO of an extreme Kerr
        black hole (`a=m`)::

            sage: EKBH = KerrBH(m, m)
            sage: EKBH.orbital_angular_velocity(EKBH.isco_radius())
            1/2/m

        """
        m = self._m
        a = self._a
        # Eq. (2.16) in Bardeen, Press & Teukolsky, ApJ 178, 347 (1972)
        three_halves = QQ(3)/QQ(2)
        sm = sqrt(m)
        if retrograde:
            return - sm / (r**three_halves - a * sm)
        return sm / (r**three_halves + a * sm)

    def orbital_frequency(self, r, retrograde=False):
        r"""
        Return the orbital frequency of a circular orbit.

        The frequency `f` of a circular orbit of Boyer-Lindquist
        radial coordinate `r` around a Kerr black hole of parameters `(m, a)`
        is `f := \Omega/(2\pi)`, where `\Omega` is given by Eq. :eq:`Omega`.

        INPUT:

        - ``r`` -- Boyer-Lindquist radial coordinate `r` of the circular orbit
        - ``retrograde`` -- (default: ``False``) boolean determining whether
          the orbit is retrograde or prograde

        OUTPUT:

        - orbital frequency `f`

        EXAMPLES::

            sage: from kerrgeodesic_gw import KerrBH
            sage: a, m, r = var('a m r')
            sage: BH = KerrBH(a, m)
            sage: BH.orbital_frequency(r)
            1/2*sqrt(m)/(pi*(a*sqrt(m) + r^(3/2)))
            sage: BH.orbital_frequency(r, retrograde=True)
            1/2*sqrt(m)/(pi*(a*sqrt(m) - r^(3/2)))
            sage: KerrBH(0.9).orbital_frequency(4.)  # tol 1.0e-13
            0.0178825778754939
            sage: KerrBH(0.9).orbital_frequency(float(4))  # tol 1.0e-13
            0.0178825778754939

        Orbital angular velocity around a Schwarzschild black hole::

            sage: KerrBH(0, m).orbital_frequency(r)
            1/2*sqrt(m)/(pi*r^(3/2))


        Orbital angular velocity on the prograde ISCO of an extreme Kerr
        black hole (`a=m`)::

            sage: EKBH = KerrBH(m, m)
            sage: EKBH.orbital_frequency(EKBH.isco_radius())
            1/4/(pi*m)

        """
        tpi = 2*pi
        try:
            par = r.parent()
            tpi = par(tpi)
        except AttributeError:
            tpi = type(r)(tpi)
        return self.orbital_angular_velocity(r, retrograde=retrograde) / tpi

    def roche_volume(self, r0, k_rot):
        r"""
        Roche volume of a star on a given circular orbit.

        The Roche volume depends on the rotational parameter

        .. MATH::

            k_\omega := \frac{\omega}{\Omega}

        where `\omega` is the angular velocity of the star (assumed to be a
        rigid rotator) with respect to some inertial frame and `\Omega` is
        the orbital angular velocity (cf. :meth:`orbital_angular_velocity`).
        The Roche volume is computed according to formulas provided by Dai
        & Blandford, Mon. Not. Roy. Astron. Soc. **434**, 2948 (2013),
        :doi:`10.1093/mnras/stt1209`.

        INPUT:

        - ``r0`` -- Boyer-Lindquist radial coordinate `r` of the circular orbit
        - ``k_rot`` -- rotational parameter `k_\omega` defined above

        OUPUT:

        - the dimensionless quantity `V_R / (\mu M^2)`, where `V_R` is the
          Roche volume, `\mu` the mass of the star and `M` the mass of the
          central black hole

        EXAMPLES:

        Roche volume around a Schwarzschild black hole::

            sage: from kerrgeodesic_gw import KerrBH
            sage: BH = KerrBH(0)
            sage: BH.roche_volume(6, 0)  # tol 1.0e-13
            98.49600000000001

        Comparison with  Eq. (26) of Dai & Blandford (2013)
        :doi:`10.1093/mnras/stt1209`::

            sage: _ - 0.456*6^3  # tol 1.0e-13
            0.000000000000000

        Case `k_\omega=1`::

            sage: BH.roche_volume(6, 1)  # tol 1.0e-13
            79.145115913556

        Comparison with  Eq. (26) of Dai & Blandford (2013)::

            sage: _ - 0.456/(1+1/4.09)*6^3  # tol 1.0e-13
            0.000000000000000

        Newtonian limit::

            sage: BH.roche_volume(1000, 0)  # tol 1.0e-13
            681633403.5759227

        Comparison with  Eq. (10) of Dai & Blandford (2013)::

            sage: _ - 0.683*1000^3  # tol 1.0e-13
            -1.36659642407727e6

        Roche volume around a rapidly rotating Kerr black hole::

            sage: BH = KerrBH(0.9)
            sage: rI = BH.isco_radius()
            sage: BH.roche_volume(rI, 0)  # tol 1.0e-13
            5.70065302837734

        Comparison with  Eq. (26) of Dai & Blandford (2013)::

            sage: _ - 0.456*rI^3  # tol 1.0e-13
            0.000000000000000

        Case `k_\omega=1`::

            sage: BH.roche_volume(rI, 1)  # tol 1.0e-13
            4.58068190295940

        Comparison with  Eq. (26) of Dai & Blandford (2013)::

            sage: _ - 0.456/(1+1/4.09)*rI^3  # tol 1.0e-13
            0.000000000000000

        Newtonian limit::

            sage: BH.roche_volume(1000, 0)  # tol 1.0e-13
            6.81881451514361e8

        Comparison with  Eq. (10) of Dai & Blandford (2013)::

            sage: _ - 0.683*1000^3  # tol 1.0e-13
            -1.11854848563898e6

        """
        # Newtonian Roche volume
        #   Eq. (10) of Dai & Blandford, MNRAS 434, 2948 (2013)
        VN = 0.683/(1. + k_rot/2.78)*r0**3
        # Roche volume at ISCO
        #   Eq. (26) of Dai & Blandford, MNRAS 434, 2948 (2013)
        VI = 0.456/(1. + k_rot/4.09)*r0**3
        # Final result
        #   Eq. (27) of Dai & Blandford, MNRAS 434, 2948 (2013)
        asm = self._a / self._m
        Fak = - 23.3 + 13.9/(k_rot + 2.8) \
              + (23.8 - 14.8/(2.8 + k_rot))*(1. - asm)**0.02 \
              + (0.9 - 0.4/(2.6 + k_rot))*(1. - asm)**(-0.16)
        x = r0 * self._m / self.isco_radius()
        return VN - (VN - VI)/(x**0.5 + Fak*(x - 1.))