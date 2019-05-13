from __future__ import division
from __future__ import print_function
from libtbx import test_utils
import libtbx.load_env
from libtbx import easy_run
import libtbx.load_env

general_tests = [
  # ions SVM
  "$D/ions/svm/tst_classifier.py",
  "$D/ions/tst_pick_ca_svm.py",
  "$D/ions/tst_pickle.py",
  # ion picking
  "$D/ions/tst_parameters.py",
  "$D/ions/tst_pick_ca.py",
  "$D/ions/tst_pick_mg.py",
  "$D/ions/tst_pick_approx_zn.py",
  "$D/ions/tst_validate_ca.py",
  "$D/ions/tst_validate_mg.py",
  "$D/ions/tst_symmetry_axis.py",
  "$D/ions/tst_utils.py",
  # TLS
  "$D/regression/tls/tst_tls.py",
  "$D/regression/tls/tst_tls_analysis.py",
  "$D/regression/tls/tst_tls_utils.py",
  "$D/regression/tls/tst_tls_optimise_amplitudes.py",
  "$D/regression/tls/tst_get_t_scheme.py",
  ["$D/regression/tls/tst_tls_refinement_fft.py", "--comprehensive", "--random_seed=2679941"],
  "$D/regression/tls/tst_u_tls_vs_u_ens_00.py",
  "$D/regression/tls/tst_u_tls_vs_u_ens_01.py",
  "$D/regression/tls/tst_u_tls_vs_u_ens_02.py",
  "$D/regression/tls/tst_u_tls_vs_u_ens_03.py",
  "$D/regression/tls/tst_u_tls_vs_u_ens_04.py",
  "$D/regression/tls/tst_tls_as_xyz.py",
  "$D/regression/tls/tst_formula_t_S_10_vs_11_2igd.py",
  "$D/regression/tls/tst_formula_t_S_10_vs_11_4muy.py",
  #
  "$D/regression/tst_angle.py",
  "$D/rotamer/tst_rotamer_eval.py",
  "$D/rotamer/tst_geostd_vs_sidechain_angles_props.py",
  "$D/monomer_library/tst_idealized_aa.py",
  "$D/regression/tst_ml_estimate.py",
  "$D/density_modification/tst_density_modification.py",
  "$D/geometry_restraints/tst_ramachandran.py",
  "$D/geometry_restraints/tst_manager.py",
  "$D/regression/tst_map_type_parser.py",
  "$D/rsr/tst.py",
  "$D/polygon/tst.py",
  "$D/polygon/tst_gui.py",
  "$D/chemical_components/tst.py",
  "$D/regression/tst_add_h_to_water.py",
  "$D/rotamer/rotamer_eval.py",
  "$D/wwpdb/tst_standard_geometry_cif.py",
  "$D/regression/tst_pdbtools.py",
  "$D/real_space/tst.py",
  "$D/ias/tst_ias.py",
  "$D/refinement/tst_fit_rotamers.py",
  ["$D/refinement/tst_anomalous_scatterer_groups.py", "P3"],
  "$D/refinement/tst_rigid_body.py",
  "$D/refinement/tst_rigid_body_groups_from_pdb_chains.py",
  "$D/refinement/tst_refinement_flags.py",
  "$D/geometry_restraints/torsion_restraints/tst_reference_model.py",
  "$D/geometry_restraints/torsion_restraints/tst_reference_model_ligands.py",
  # model tests, some more elsewhere in this file
  "$D/regression/model/tst_model_mtrix.py",
  "$D/regression/model/tst_model_2.py",
  "$D/regression/model/tst_model_biomt_mtrix.py",
  "$D/regression/model/tst_model_neutralize_scatterers.py",
  "$D/regression/model/tst_model_cart_ref_restraints.py",
  "$D/regression/model/tst_model_tors_ref_restraints.py",
  "$D/regression/model/tst_model_remove_alternative_conformations.py",
  "$D/regression/model/tst_model_get_vdw_radii.py",
  #
  "$D/regression/tst_fmodel.py",
  "$D/regression/tst_utils.py",
  "$D/regression/tst_alignment.py",
  ["$D/regression/tst_fmodel_fd.py", "P31"],
  "$D/maps/tst_composite_omit_map.py",
  "$D/maps/tst_composite_omit_map_2.py",
  "$D/maps/tst_composite_omit_map_3.py",
  "$D/maps/tst_correlation.py",
  "$D/regression/ncs/tst_ncs_utils.py",
  "$D/regression/ncs/tst_ncs_restraints_group_list.py",
  "$D/regression/ncs/tst_ncs_search.py",
  "$D/regression/ncs/tst_ncs_search_flips.py",
  "$D/regression/ncs/tst_restraints.py",
  "$D/regression/tst_geometry_minimization.py",
  ["$D/ncs/ncs.py", "exercise"],
  "$D/regression/tst_adp_restraints.py",
  "$D/regression/tst_metal_link_1.py",
  # Xtriage
  "$D/scaling/tst_scaling.py",
  "$D/scaling/tst_outlier.py",
  "$D/scaling/tst_absences.py",
  "$D/scaling/tst_xtriage.py",
  "$D/scaling/tst_xtriage_twin_analyses.py",
  "$D/scaling/matthews.py",
  "$D/scaling/absence_likelihood.py",
  ["$D/scaling/thorough_outlier_test.py", "P21"],
  "$D/twinning/probabalistic_detwinning.py",
  #"$D/scaling/tst_xtriage_massage_data.py",
  # monomer library
  "$D/monomer_library/tst_rna_sugar_pucker_analysis.py",
  "$D/monomer_library/tst_cif_types.py",
  "$D/monomer_library/tst_motif.py",
  "$D/monomer_library/tst_cif_triage.py",
  "$D/monomer_library/tst_rotamer_utils.py",
  "$D/monomer_library/tst_selection.py",
  "$D/monomer_library/tst_tyr_from_gly_and_bnz.py",
  "$D/monomer_library/tst_pdb_interpretation.py",
  "$D/monomer_library/tst_rna_dna_interpretation.py",
  "$D/monomer_library/tst_protein_interpretation.py",
  "$D/monomer_library/tst_pdb_interpretation_ncs_processing.py",
  "$D/monomer_library/tst_geo_reduce_for_tardy.py",
  "$D/monomer_library/tst_chg.py",
  "$D/monomer_library/tst_neutron_distance.py",
  #
  "$D/regression/tst_altloc_remediate.py",
  "$D/hydrogens/build_hydrogens.py",
  "$D/hydrogens/tst.py",
  "$D/hydrogens/tst_add_hydrogen.py",
  "$D/hydrogens/tst_add_hydrogen_2.py",
  "$D/hydrogens/tst_validate_H.py",
  "$D/hydrogens/tst_connectivity.py",
  "$D/hydrogens/tst_riding_coefficients.py",
  "$D/hydrogens/tst_riding_manager.py",
  "$D/hydrogens/tst_parameterization_1.py",
  "$D/hydrogens/tst_parameterization_2.py",
  "$D/hydrogens/tst_parameterization_3.py",
  "$D/hydrogens/tst_parameterization_4.py",
  "$D/hydrogens/tst_parameterization_5.py",
  "$D/hydrogens/tst_parameterization_6.py",
  "$D/hydrogens/tst_parameterization_7.py",
  "$D/hydrogens/tst_parameterization_8.py",
  "$D/hydrogens/tst_riding_fd_1.py",
  "$D/hydrogens/tst_riding_fd_2.py",
  "$D/hydrogens/tst_riding_fd_3.py",
  "$D/hydrogens/tst_riding_fd_4.py",
  "$D/hydrogens/tst_riding_fd_5.py",
  "$D/hydrogens/tst_riding_minimize.py",
  "$D/max_lik/tst_maxlik.py",
  "$D/masks/tst_masks.py",
  "$D/masks/tst_asu_mask.py",
  "$D/max_lik/tst_max_lik.py",
  "$D/dynamics/tst_cartesian_dynamics.py",
  "$D/dynamics/tst_sa.py",
  #
  "$D/examples/f_model_manager.py",
  # Bulk solvent
  "$D/bulk_solvent/tst_bulk_solvent_and_scaling.py",
  "$D/bulk_solvent/tst_fit_kexpb_to_ktotal.py",
  "$D/bulk_solvent/tst_scaler.py",
  "$D/bulk_solvent/tst_flat_nonuniform.py",
  "$D/bulk_solvent/tst_aniso_scaler.py",
  "$D/bulk_solvent/tst_kb_sol_u_star_fd.py",
  #
  "$D/invariant_domain.py",
  # restraints
  "$D/regression/tst_psi_phi_extraction.py",
  "$D/secondary_structure/tst.py",
  "$D/secondary_structure/tst_insertion_codes.py",
  "$D/secondary_structure/tst_segid.py",
  "$D/geometry_restraints/tst_reference_coordinate.py",
  "$D/geometry_restraints/tst_reference_coordinate2.py",
  "$D/geometry_restraints/tst_c_beta_restraints.py",
  "$D/geometry_restraints/torsion_restraints/tst_torsion_ncs.py",
  "$D/conformation_dependent_library/tst_cdl.py",
  "$D/conformation_dependent_library/tst_cdl_esd.py",
  "$D/conformation_dependent_library/tst_rdl.py",
  "$D/conformation_dependent_library/tst_hpdl.py",
  "$D/conformation_dependent_library/tst_pH_mechanism.py",
  "$D/regression/tst_find_ss_structure.py",
  "$D/regression/tst_fix_rotamer_outliers.py",
  "$D/regression/tst_chain_comparison.py",
  "$D/regression/tst_regularize_from_pdb.py",
  "$D/regression/tst_find_ncs.py",
  "$D/regression/tst_minimize_chain.py",
  "$D/regression/tst_sequence_validation.py",
  "$D/regression/tst_prune_model.py",
  "$D/regression/tst_real_space_correlation.py",
  "$D/regression/tst_examples.py",
  "$D/regression/tst_sort_hetatms.py",
  # real-space tools
  "$D/refinement/real_space/tst_aa_residue_axes_and_clusters.py",
  "$D/refinement/real_space/tst_fit_residue_0.py",
  "$D/refinement/real_space/tst_fit_residue_0H.py",
  "$D/refinement/real_space/tst_fit_residue_1.py",
  "$D/refinement/real_space/tst_fit_residue_1H.py",
  "$D/refinement/real_space/tst_fit_residue_2.py",
  "$D/refinement/real_space/tst_fit_residue_3.py",
  "$D/refinement/real_space/tst_fit_residue_4.py",
  "$D/refinement/real_space/tst_fit_residue_5.py",
  "$D/refinement/real_space/tst_fit_residue_6.py",
  "$D/refinement/real_space/tst_fit_residues_1.py",
  "$D/refinement/real_space/tst_fit_residues_1H.py",
  "$D/refinement/real_space/tst_fit_residues_2.py",
  "$D/refinement/real_space/tst_fit_residues_3.py",
  "$D/refinement/real_space/tst_fit_residues_4.py",
  "$D/refinement/real_space/tst_fit_residues_5.py",
  "$D/refinement/real_space/tst_fit_residues_6.py",
  "$D/refinement/real_space/tst_fit_residues_selection.py",
  "$D/refinement/real_space/tst_fit_water.py",
  "$D/refinement/real_space/tst_flipbase.py",
  "$D/refinement/real_space/tst_individual_sites_1.py",
  "$D/refinement/real_space/tst_individual_sites_2.py",
  "$D/refinement/real_space/tst_individual_sites_3.py",
  "$D/refinement/real_space/tst_monitor.py",
  "$D/refinement/real_space/tst_rigid_body.py",
  "$D/refinement/real_space/tst_weight.py",
  #
  "$D/idealized_aa_residues/tst.py",
  #
  "$D/regression/tst_dssp.py",
  "$D/regression/tst_validation_summary.py",
  "$D/regression/tst_maps_misc.py",
  "$D/regression/tst_cablam.py",
  "$D/regression/tst_anomalous_substructure.py",
  "$D/regression/tst_map_coeffs_simple.py",
  #
  "$D/regression/tst_fmodel_no_cryst1.py",
  "$D/regression/tst_fmodel_misc.py",
  "$D/regression/tst_isomorphous_difference_misc.py",
  "$D/regression/tst_dynamics_cli.py",
  "$D/ligands/tst_xtal_screens.py",
  "$D/regression/tst_mtz2map.py",
  # ringer
  "$D/regression/tst_ringer.py",
  "$D/ringer/tst_emringer.py",
  "$D/ringer/tst_em_rscc.py",
  # validation/molprobity
  "$D/validation/regression/tst_molprobity_arguments.py",
  "$D/validation/regression/tst_waters.py",
  "$D/validation/regression/tst_keep_hydrogens.py",
  "$D/validation/regression/tst_mp_geo.py",
  "$D/validation/regression/tst_rotalyze.py",
  "$D/validation/regression/tst_ramalyze.py",
  "$D/validation/regression/tst_ramalyze2.py",
  "$D/validation/regression/tst_clashscore.py",
  "$D/validation/regression/tst_restraints.py",
  "$D/validation/regression/tst_omegalyze.py",
  "$D/validation/regression/tst_rna_validate.py",
  "$D/validation/regression/tst_model_properties.py",
  "$D/validation/regression/tst_molprobity_2.py",
  "$D/validation/regression/tst_molprobity_3.py",
  "$D/validation/regression/tst_hydrogen_addition_clashscore.py",
  "$D/validation/regression/tst_symmetry_SS.py",
  "$D/validation/regression/tst_do_flips_clashscore.py",
  "$D/validation/regression/tst_find_region_max_value.py",
  #
  "$D/refinement/tst_select_best_starting_model.py",
  "$D/regression/tst_refine_anomalous_substructure.py",
  "$D/regression/tst_helix_sheet_recs_as_pdb_files.py",
  "$D/regression/tst_command_line_input.py",
  "$D/regression/tst_cif_as_mtz_wavelengths.py",
  "$D/building/tst_extend_sidechains.py",
  "$D/building/tst_extend_sidechains_2.py",
  # alt confs
  "$D/building/alternate_conformations/tst_backrub_conformers.py",
  "$D/building/alternate_conformations/tst_shear_conformers.py",
  "$D/building/alternate_conformations/tst_partial_omit_map.py",
  "$D/disorder/tst.py",
  "$D/disorder/tst_backbone.py",
  "$D/disorder/tst_analyze_model.py",
  #
  "$D/refinement/tst_group.py",
  "$D/refinement/tst_group_2.py",
  "$D/secondary_structure/build/tst_1.py",
  "$D/secondary_structure/build/tst_2.py",
  "$D/secondary_structure/build/tst_3.py",
  "$D/secondary_structure/build/tst_io.py",
  "$D/secondary_structure/build/tst_ss_id_ncs.py",
  "$D/regression/tst_loop_closure.py",
  "$D/regression/model_idealization/tst_nomap_01.py",
  "$D/regression/model_idealization/tst_nomap_02.py",
  "$D/regression/model_idealization/tst_nomap_03.py",
  "$D/regression/model_idealization/tst_nomap_04.py",
  "$D/regression/model_idealization/tst_withmap_01.py",
  "$D/regression/model_idealization/tst_withmap_02.py",
  "$D/regression/model_idealization/tst_withmap_03.py",
  "$D/regression/model_idealization/tst_withmap_04.py",
  "$D/regression/model_idealization/tst_withmap_05.py",
  "$D/regression/model_idealization/tst_withmap_06.py",
  "$D/regression/model_idealization/tst_ligands.py",
  "$D/regression/model_idealization/tst_with_mtz.py",
  "$D/regression/model_idealization/tst_ext_map_01.py",
  "$D/utils/tst_switch_rotamers.py",
  "$D/refinement/tst_occupancy_selections.py",
  "$D/regression/ncs/tst_minimization_ncs_constraints.py",
  "$D/regression/ncs/tst_minimization_ncs_constraints2.py",
  "$D/regression/ncs/tst_minimization_ncs_constraints3.py",
  "$D/regression/ncs/tst_minimization_ncs_constraints_real_space.py",
  "$D/monomer_library/tst_correct_hydrogens.py",
  # automatic linking
  "$D/monomer_library/tst_superpose_ideal.py",
  #
  "$D/ions/tst_pick_ca_svm.py",
  "$D/scaling/tst_plan_sad_experiment.py",
  #
  "$D/regression/tst_models_to_from_chains.py",
  "$D/regression/tst_helix_sheet_recs_as_pdb_files.py",
  # tNCS
  "$D/regression/tncs/tst_pair.py",
  "$D/regression/tncs/tst_epsfac_and_radius.py",
  "$D/regression/tncs/tst_fd.py",
  "$D/regression/tncs/tst_moments.py",
  #
  "$D/regression/tst_rank_scale_map.py",
  "$D/regression/tst_polder.py",
  "$D/regression/tst_polder_1.py",
  "$D/regression/tst_polder_2.py",
  "$D/regression/tst_polder_3.py",
  "$D/regression/tst_polder_box.py",
  "$D/regression/tst_polder_ccs.py",
  "$D/regression/tst_map_model_cc.py",
  "$D/regression/tst_model_map.py",
  #
  "$D/regression/tst_validate_ligands.py",
  #
  "$D/regression/tst_cis_trans_peptide_link.py",
  "$D/regression/tst_apply_cif_restraints.py",
  "$D/regression/tst_multi_residue_class.py",
  "$D/regression/tst_flip_symmetric.py",
  "$D/regression/tst_superpose.py",
  "$D/monomer_library/tst_server.py",
  #
  "$D/geometry/tests/tst_altloc.py",
  "$D/geometry/tests/tst_asa.py",
  "$D/geometry/tests/tst_clash.py",
  "$D/geometry/tests/tst_indexing.py",
  "$D/geometry/tests/tst_shared_types.py",
  "$D/geometry/tests/tst_sphere_surface_sampling.py",
  "$D/geometry/tests/tst_topology.py",
  #
  "$D/wwpdb/tst_rcsb_web_services.py",
  "$D/wwpdb/tst_utils.py",
  "$D/monomer_library/tst_all_cif_files.py",
  "$D/refinement/tst_misc.py",
  "$D/refinement/tst_real_space_simple.py",
  "$D/scaling/tst_bayesian_estimator.py",
  "$D/scaling/tst_mean_f_rms_f.py",
  "$D/scaling/tst_sigmaa.py",
  "$D/scaling/tst_massage_data.py",
  "$D/ions/tst_geometries.py",
  "$D/ions/tst_pick_k.py",
  "$D/ions/tst_environment.py",
  "$D/regression/tst_table_one.py",
  "$D/regression/tst_msa.py",
  "$D/regression/tst_build_alt_confs.py",
  "$D/regression/tst_cc_star.py",
  "$D/regression/tst_fmodel_2.py",
  "$D/regression/tst_rigid_bond_test.py",
  "$D/validation/regression/tst_cablam.py",
  "$D/building/tst_make_library.py",
  "$D/regression/real_space_refine_chain/tst_00.py",
  "$D/regression/real_space_refine_chain/tst_01.py",
  "$D/conformation_dependent_library/tst_omega_cdl.py",
  "$D/regression/fix_cablam/tst_basic_cl_operations.py",
  "$D/regression/fix_cablam/tst_single_outliers_surroundings.py",
  "$D/regression/fix_cablam/tst_one_resid_rotation.py",
  "$D/regression/fix_cablam/tst_insertion_codes.py",
  #
  "$D/regression/tst_scattering_type_registry.py"
  ]

probe_tests = [
  "$D/regression/pdb_interpretation/tst_edits.py",
  "$D/regression/tst_add_arrows_on_plot.py",
  "$D/regression/model/tst_model.py",
  "$D/regression/tst_reduce_timeout.py",
  "$D/regression/tst_altloc_chain_break.py",
  "$D/regression/ncs/tst_geometry_minimization_ncs_constraints.py",
  "$D/regression/tst_clashes.py",
  "$D/validation/regression/tst_cbetadev.py",
  "$D/regression/tst_statistics_output.py",
  "$D/regression/tst_geo_min_restraints_phil.py",
  "$D/regression/tst_model_vs_map.py",
  # validation/molprobity
  "$D/validation/regression/tst_nqh_minimize.py",
  "$D/validation/regression/tst_molprobity_1.py",
  "$D/validation/regression/tst_molprobity_4.py",
  "$D/validation/regression/tst_experimental.py",
  "$D/validation/regression/tst_cablam_2.py",
  # automatic linking
  ["$D/monomer_library/tst_metal_coordination.py", "1"],
  ["$D/monomer_library/tst_metal_coordination.py", "2"],
  ["$D/monomer_library/tst_linking.py", "1"],
  ["$D/monomer_library/tst_linking.py", "2"],
  ["$D/monomer_library/tst_linking.py", "3"],
  ["$D/monomer_library/tst_linking.py", "4"],
  ["$D/monomer_library/tst_linking.py", "5"],
  ["$D/monomer_library/tst_linking.py", "6"],
  ["$D/monomer_library/tst_linking.py", "7"],
  ["$D/monomer_library/tst_linking.py", "8"],
  ["$D/monomer_library/tst_linking.py", "9"],
  ["$D/monomer_library/tst_linking.py", "10"],
  ["$D/monomer_library/tst_linking.py", "11"],
  ["$D/monomer_library/tst_linking.py", "12"],
  ["$D/monomer_library/tst_linking.py", "13"],
  ["$D/monomer_library/tst_linking.py", "14"],
  ["$D/monomer_library/tst_linking.py", "15"],
  ["$D/monomer_library/tst_linking.py", "16"],
  ["$D/monomer_library/tst_linking.py", "17"],
  ["$D/monomer_library/tst_linking.py", "18"],
  ["$D/monomer_library/tst_linking.py", "19"],
  ["$D/monomer_library/tst_linking.py", "20"],
  ["$D/monomer_library/tst_linking.py", "21"],
  ["$D/monomer_library/tst_linking.py", "22"],
  ["$D/monomer_library/tst_linking.py", "23"],
  ["$D/monomer_library/tst_linking.py", "24"],
  ["$D/monomer_library/tst_linking.py", "25"],
  ["$D/monomer_library/tst_linking.py", "26"],
  ["$D/monomer_library/tst_linking.py", "27"],
  ["$D/monomer_library/tst_linking.py", "28"],
  ["$D/monomer_library/tst_linking.py", "29"],
  ["$D/monomer_library/tst_linking.py", "30"],
  ["$D/monomer_library/tst_linking.py", "31"],
  ["$D/monomer_library/tst_linking.py", "32"],

]

if libtbx.env.has_module(name="probe"):
  tst_list = tuple(general_tests + probe_tests)
else:
  print("Skipping %d probe tests: probe not configured"%len(probe_tests))
  tst_list = tuple(general_tests)

def run():
  assert easy_run.call("libtbx.find_untested mmtbx True")==0
  build_dir = libtbx.env.under_build("mmtbx")
  dist_dir = libtbx.env.dist_path("mmtbx")
  test_utils.run_tests(build_dir, dist_dir, tst_list)

if (__name__ == "__main__"):
  run()
