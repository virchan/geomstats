"""Unit tests for visualization."""

import matplotlib
import matplotlib.pyplot as plt

import geomstats.backend as gs
import geomstats.tests
import geomstats.visualization as visualization
from geomstats.geometry.hyperbolic import Hyperbolic
from geomstats.geometry.hypersphere import Hypersphere
from geomstats.geometry.matrices import Matrices
from geomstats.geometry.poincare_half_space import PoincareHalfSpace
from geomstats.geometry.pre_shape import PreShapeSpace
from geomstats.geometry.special_euclidean import SpecialEuclidean
from geomstats.geometry.special_orthogonal import SpecialOrthogonal, \
    _SpecialOrthogonalMatrices

matplotlib.use('Agg')  # NOQA


class TestVisualization(geomstats.tests.TestCase):
    def setUp(self):
        self.n_samples = 10
        self.SO3_GROUP = SpecialOrthogonal(n=3, point_type='vector')
        self.SE3_GROUP = SpecialEuclidean(n=3, point_type='vector')
        self.S1 = Hypersphere(dim=1)
        self.S2 = Hypersphere(dim=2)
        self.H2 = Hyperbolic(dim=2)
        self.H2_half_plane = PoincareHalfSpace(dim=2)
        self.M32 = Matrices(m=3, n=2)
        self.S32 = PreShapeSpace(k_landmarks=3, m_ambient=2)
        self.KS = visualization.KendallSphere()

        plt.figure()

    @staticmethod
    def test_tutorial_matplotlib():
        visualization.tutorial_matplotlib()

    def test_plot_points_so3(self):
        points = self.SO3_GROUP.random_uniform(self.n_samples)
        visualization.plot(points, space='SO3_GROUP')

    def test_plot_points_se3(self):
        points = self.SE3_GROUP.random_point(self.n_samples)
        visualization.plot(points, space='SE3_GROUP')

    def test_draw_pre_shape(self):
        self.KS.draw()

    def test_plot_points_pre_shape(self):
        points = self.S32.random_point(self.n_samples)
        visualization.plot(points, space='S32')
        points = self.M32.random_point(self.n_samples)
        visualization.plot(points, space='M32')
        self.KS.clear_points()

    def test_plot_curve_pre_shape(self):
        base_point = self.S32.random_point()
        vec = self.S32.random_point()
        tangent_vec = self.S32.to_tangent(vec, base_point)
        times = gs.linspace(0, .5, 1000)
        speeds = gs.array([-t * tangent_vec for t in times])
        points = self.S32.ambient_metric.exp(speeds, base_point)
        self.KS.add_points(points)
        self.KS.draw_curve()
        self.KS.clear_points()

    def test_plot_vector_pre_shape(self):
        base_point = self.S32.random_point()
        vec = self.S32.random_point()
        tangent_vec = self.S32.to_tangent(vec, base_point)
        self.KS.draw_vector(tangent_vec, base_point)

    def test_coordinates_pre_shape(self):
        points = self.S32.random_point(self.n_samples)
        coords = self.KS.convert_to_spherical_coordinates(points)
        x = gs.array([coord[0] for coord in coords])
        y = gs.array([coord[1] for coord in coords])
        z = gs.array([coord[2] for coord in coords])
        result = x ** 2 + y ** 2 + z ** 2
        expected = .25 * gs.ones(self.n_samples)
        self.assertAllClose(result, expected)

    def test_rotation_pre_shape(self):
        theta = gs.random.rand()
        phi = gs.random.rand()
        rot = self.KS.rotation(theta, phi)
        result = _SpecialOrthogonalMatrices(3).belongs(rot)
        expected = True
        self.assertAllClose(result, expected)

    @geomstats.tests.np_and_pytorch_only
    def test_plot_points_s1(self):
        points = self.S1.random_uniform(self.n_samples)
        visualization.plot(points, space='S1')

    def test_plot_points_s2(self):
        points = self.S2.random_uniform(self.n_samples)
        visualization.plot(points, space='S2')

    def test_plot_points_h2_poincare_disk(self):
        points = self.H2.random_point(self.n_samples)
        visualization.plot(points, space='H2_poincare_disk')

    def test_plot_points_h2_poincare_half_plane_ext(self):
        points = self.H2.random_point(self.n_samples)
        visualization.plot(points, space='H2_poincare_half_plane',
                           point_type='extrinsic')

    def test_plot_points_h2_poincare_half_plane_none(self):
        points = self.H2_half_plane.random_point(self.n_samples)
        visualization.plot(points, space='H2_poincare_half_plane')

    def test_plot_points_h2_poincare_half_plane_hs(self):
        points = self.H2_half_plane.random_point(self.n_samples)
        visualization.plot(points, space='H2_poincare_half_plane',
                           point_type='half_space')

    def test_plot_points_h2_klein_disk(self):
        points = self.H2.random_point(self.n_samples)
        visualization.plot(points, space='H2_klein_disk')

    @staticmethod
    def test_plot_points_se2():
        points = SpecialEuclidean(n=2, point_type='vector').random_point(4)
        visu = visualization.SpecialEuclidean2(points, point_type='vector')
        ax = visu.set_ax()
        visu.draw(ax)