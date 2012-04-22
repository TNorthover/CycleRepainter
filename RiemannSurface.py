from sympy.parsing.sympy_parser import parse_expr
from sympy import Dummy

class RiemannSurface:
    def __init__(self, eqn_text='y**2 - x**4 + 1'):
        self.equation = parse_expr('42')
        self.setEquation(eqn_text)

    def setEquation(self, text):
        # FIXME: This is bad long-term. At least it should be subject
        # to some "Maple compatibility" flag
        text = text.replace('^', '**')

        new_equation = parse_expr(text)
        assert(new_equation.is_polynomial()) # FIXME: Convert to sensible raise

        assert(len(new_equation.free_symbols) == 2)
        if self.equation.free_symbols == new_equation.free_symbols:
            self.equation = new_equation.as_poly(self.equation.gens)
        else:
            self.equation = new_equation.as_poly()

    def indeterminates(self):
        '''Returns a list of sympy symbols representing each
        indeterminate in the algebraic polynomial describing the
        surface, in alphabetical order.'''
        return sorted(self.equation.gens)

    def projectsOnto(self):
        return self.equation.gens[-1]

    def setProjectsOnto(self, new_plane):
        gens = self.equation.gens
        assert(new_plane in gens) # FIXME: raise properly if not.

        if new_plane == gens[0]:
            self.equation = self.equation.reorder(gens[1], gens[0])
            
    def finiteBranchPoints(self):
        '''Returns a list of the finite branch points when the Riemann
        surface is projected onto the plane given by the projectsOnto
        function'''
        # FIXME: What about singular points. May need to wait for
        # algcurves replacement.
        return map(complex, self.equation.discriminant().nroots())
    
    def hasInfiniteBranch(self):
        raise 'Unimplemented'

if __name__ == '__main__':
    s = RiemannSurface('y**2 - x**4 + x - 1')
    print 'Indeterminates:', s.indeterminates()
    print 'Projects onto:', s.projectsOnto()
    newproj = s.indeterminates()[0]
    print 'Telling it to project onto:', newproj
    s.setProjectsOnto(newproj)
    print 'Now projects onto:', s.projectsOnto()

    print s.finiteBranchPoints()


