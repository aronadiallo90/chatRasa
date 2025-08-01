-- DROP SCHEMA dbo;

CREATE SCHEMA dbo;
-- referentiel_fudpe_new.dbo.DossierTest definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.DossierTest;

CREATE TABLE referentiel_fudpe_new.dbo.DossierTest (
	DossierID int IDENTITY(1,1) NOT NULL,
	CodeDossier varchar(50) COLLATE French_CI_AS NOT NULL,
	DateReception date NOT NULL,
	TypeDossier varchar(100) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK__DossierT__CABB1DF021D69855 PRIMARY KEY (DossierID)
);


-- referentiel_fudpe_new.dbo.PARTICIPANTINSTANCE_140324 definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.PARTICIPANTINSTANCE_140324;

CREATE TABLE referentiel_fudpe_new.dbo.PARTICIPANTINSTANCE_140324 (
	PART_INST_ID bigint NOT NULL,
	PART_INST_DATE_CREATED datetime2 NULL,
	PART_INST_DATE_UPDATED datetime2 NULL,
	PART_INST_CODE_ACTION varchar(255) COLLATE French_CI_AS NULL,
	PART_INST_CODE_FONCTION varchar(255) COLLATE French_CI_AS NULL,
	PART_INST_CODE_STRUCTURE varchar(255) COLLATE French_CI_AS NULL,
	ACT_INST_ID bigint NULL
);


-- referentiel_fudpe_new.dbo.act_usr_code definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.act_usr_code;

CREATE TABLE referentiel_fudpe_new.dbo.act_usr_code (
	agt_id int NOT NULL,
	act_usr_code bigint NULL,
	username_id bigint NOT NULL,
	agt_matricule_solde varchar(15) COLLATE French_CI_AS NULL,
	username varchar(255) COLLATE French_CI_AS NOT NULL,
	usr_login varchar(255) COLLATE French_CI_AS NULL,
	agt_prenom varchar(255) COLLATE French_CI_AS NULL,
	agt_nom varchar(255) COLLATE French_CI_AS NULL,
	usr_prenom varchar(255) COLLATE French_CI_AS NULL,
	usr_nom varchar(255) COLLATE French_CI_AS NULL,
	usr_bon_code varchar(100) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.acteStable definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.acteStable;

CREATE TABLE referentiel_fudpe_new.dbo.acteStable (
	act_id int IDENTITY(50684612,1) NOT NULL,
	act_is_projet bit NOT NULL,
	act_numero_projet varchar(255) COLLATE French_CI_AS NULL,
	act_date_projet date NULL,
	act_numero_acte varchar(255) COLLATE French_CI_AS NULL,
	act_date_acte date NULL,
	act_observation varchar(255) COLLATE French_CI_AS NULL,
	act_ref_GED varchar(255) COLLATE French_CI_AS NULL,
	act_prise_en_compte_solde bit NOT NULL,
	act_ref_syst_externe varchar(255) COLLATE French_CI_AS NULL,
	act_tac_id int NOT NULL,
	act_act_lie int NULL,
	act_initiateur_id int NULL,
	act_process_instance_id int NULL,
	act_date_created datetime2 NULL,
	act_date_updated datetime2 NULL,
	act_deleted bit NOT NULL,
	act_date_deleted datetime2 NULL,
	act_etat_id int NULL,
	act_chemin_word varchar(255) COLLATE French_CI_AS NULL,
	act_numero_etape_circuit int NULL,
	act_str_parent_initiateur varchar(100) COLLATE French_CI_AS NULL,
	act_str_initiateur varchar(100) COLLATE French_CI_AS NULL,
	act_str_projet_acte varchar(100) COLLATE French_CI_AS NULL,
	act_is_rejet numeric(38,0) NULL,
	act_fonct_initiateur varchar(100) COLLATE French_CI_AS NULL,
	act_str_parent_projet_acte varchar(100) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.acte_agent_bkp2302025 definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.acte_agent_bkp2302025;

CREATE TABLE referentiel_fudpe_new.dbo.acte_agent_bkp2302025 (
	act_agt_id int IDENTITY(1,1) NOT NULL,
	act_agt_act_id int NOT NULL,
	act_agt_agt_id int NOT NULL,
	act_agt_cce_id int NULL,
	act_agt_fct_code varchar(20) COLLATE French_CI_AS NULL,
	act_agt_str_code varchar(20) COLLATE French_CI_AS NULL,
	act_agt_spe_code varchar(7) COLLATE French_CI_AS NULL,
	act_agt_pos_code varchar(3) COLLATE French_CI_AS NULL,
	act_agt_date_effet date NOT NULL,
	act_agt_date_created datetime2 NULL,
	act_agt_date_updated datetime2 NULL,
	act_agt_deleted bit NOT NULL,
	act_agt_date_deleted datetime2 NULL,
	act_agt_dip_code varchar(10) COLLATE French_CI_AS NULL,
	act_agt_session_diplome char(4) COLLATE French_CI_AS NULL,
	act_agt_date_obtention_diplome date NULL,
	act_poste_budgetaire_libere varchar(255) COLLATE French_CI_AS NULL,
	act_agt_date_entree_service date NULL,
	act_observations varchar(255) COLLATE French_CI_AS NULL,
	act_agt_pays_code varchar(20) COLLATE French_CI_AS NULL,
	act_agt_pays_id int NULL,
	act_agt_date_avis_mutation date NULL,
	act_agt_note_globale varchar(255) COLLATE French_CI_AS NULL,
	act_agt_taux_mensuel decimal(10,0) NULL,
	act_agt_agt_remplace_id int NULL,
	act_agt_motif_remplacement varchar(250) COLLATE French_CI_AS NULL,
	act_poste_budgetaire_accueil varchar(255) COLLATE French_CI_AS NULL,
	act_agt_date_debut date NULL,
	act_agt_date_fin date NULL,
	act_agt_duree int NULL,
	act_agt_date_deces date NULL,
	act_agt_lieu_deces varchar(255) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.acte_bkp2302025 definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.acte_bkp2302025;

CREATE TABLE referentiel_fudpe_new.dbo.acte_bkp2302025 (
	act_id int IDENTITY(50684612,1) NOT NULL,
	act_is_projet bit NOT NULL,
	act_numero_projet varchar(255) COLLATE French_CI_AS NULL,
	act_date_projet date NULL,
	act_numero_acte varchar(255) COLLATE French_CI_AS NULL,
	act_date_acte date NULL,
	act_observation varchar(255) COLLATE French_CI_AS NULL,
	act_ref_GED varchar(255) COLLATE French_CI_AS NULL,
	act_prise_en_compte_solde bit NOT NULL,
	act_ref_syst_externe varchar(255) COLLATE French_CI_AS NULL,
	act_tac_id int NOT NULL,
	act_act_lie int NULL,
	act_initiateur_id int NULL,
	act_process_instance_id int NULL,
	act_date_created datetime2 NULL,
	act_date_updated datetime2 NULL,
	act_deleted bit NOT NULL,
	act_date_deleted datetime2 NULL,
	act_etat_id int NULL,
	act_chemin_word varchar(255) COLLATE French_CI_AS NULL,
	act_numero_etape_circuit int NULL,
	act_str_parent_initiateur varchar(100) COLLATE French_CI_AS NULL,
	act_str_initiateur varchar(100) COLLATE French_CI_AS NULL,
	act_str_projet_acte varchar(100) COLLATE French_CI_AS NULL,
	act_is_rejet numeric(38,0) NULL,
	act_fonct_initiateur varchar(100) COLLATE French_CI_AS NULL,
	act_str_parent_projet_acte varchar(100) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.actecircuit definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.actecircuit;

CREATE TABLE referentiel_fudpe_new.dbo.actecircuit (
	act_id int IDENTITY(50684612,1) NOT NULL,
	act_is_projet bit NOT NULL,
	act_numero_projet varchar(255) COLLATE French_CI_AS NULL,
	act_date_projet date NULL,
	act_numero_acte varchar(255) COLLATE French_CI_AS NULL,
	act_date_acte date NULL,
	act_observation varchar(255) COLLATE French_CI_AS NULL,
	act_ref_GED varchar(255) COLLATE French_CI_AS NULL,
	act_prise_en_compte_solde bit NOT NULL,
	act_ref_syst_externe varchar(255) COLLATE French_CI_AS NULL,
	act_tac_id int NOT NULL,
	act_act_lie int NULL,
	act_initiateur_id int NULL,
	act_process_instance_id int NULL,
	act_date_created datetime2 NULL,
	act_date_updated datetime2 NULL,
	act_deleted bit NOT NULL,
	act_date_deleted datetime2 NULL,
	act_etat_id int NULL,
	act_chemin_word varchar(255) COLLATE French_CI_AS NULL,
	act_numero_etape_circuit int NULL,
	act_str_parent_initiateur varchar(100) COLLATE French_CI_AS NULL,
	act_str_initiateur varchar(100) COLLATE French_CI_AS NULL,
	act_str_projet_acte varchar(100) COLLATE French_CI_AS NULL,
	act_is_rejet numeric(38,0) NULL,
	act_fonct_initiateur varchar(100) COLLATE French_CI_AS NULL,
	act_str_parent_projet_acte varchar(100) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.actes_pieces definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.actes_pieces;

CREATE TABLE referentiel_fudpe_new.dbo.actes_pieces (
	act_id bigint NULL,
	chemin varchar(255) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.[action] definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.[action];

CREATE TABLE referentiel_fudpe_new.dbo.[action] (
	action_id int IDENTITY(1,1) NOT NULL,
	action_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK_action PRIMARY KEY (action_id)
);


-- referentiel_fudpe_new.dbo.agent_bkp2302025 definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.agent_bkp2302025;

CREATE TABLE referentiel_fudpe_new.dbo.agent_bkp2302025 (
	agt_id int IDENTITY(51101201,1) NOT NULL,
	agt_matricule_solde varchar(15) COLLATE French_CI_AS NULL,
	agt_cni varchar(25) COLLATE French_CI_AS NULL,
	agt_matricule_interne varchar(50) COLLATE French_CI_AS NULL,
	agt_prenom varchar(255) COLLATE French_CI_AS NULL,
	agt_nom varchar(255) COLLATE French_CI_AS NULL,
	agt_date_naissance date NULL,
	agt_lieu_naissance varchar(255) COLLATE French_CI_AS NULL,
	agt_adresse varchar(255) COLLATE French_CI_AS NULL,
	agt_genre varchar(5) COLLATE French_CI_AS NULL,
	agt_situation_matrimoniale varchar(50) COLLATE French_CI_AS NULL,
	agt_telephone varchar(15) COLLATE French_CI_AS NULL,
	agt_email varchar(255) COLLATE French_CI_AS NULL,
	agt_prenom_pere varchar(255) COLLATE French_CI_AS NULL,
	agt_prenom_mere varchar(255) COLLATE French_CI_AS NULL,
	agt_nom_mere varchar(255) COLLATE French_CI_AS NULL,
	agt_nb_enfants_charge int NULL,
	agt_date_derniere_situation date NULL,
	agt_date_derniere_position date NULL,
	agt_num_ordre varchar(255) COLLATE French_CI_AS NULL,
	agt_ref_syst_externe varchar(255) COLLATE French_CI_AS NULL,
	agt_ref_photo varchar(255) COLLATE French_CI_AS NULL,
	agt_cce_id int NULL,
	agt_pos_code varchar(3) COLLATE French_CI_AS NULL,
	agt_spe_code varchar(7) COLLATE French_CI_AS NULL,
	agt_affectation_id int NULL,
	agt_str_code varchar(20) COLLATE French_CI_AS NULL,
	agt_fct_code varchar(20) COLLATE French_CI_AS NULL,
	agt_user_id int NULL,
	agt_initiateur_id int NULL,
	agt_date_entree_service date NULL,
	agt_date_created datetime2 NULL,
	agt_date_updated datetime2 NULL,
	agt_ministere_code varchar(20) COLLATE French_CI_AS NULL,
	agt_deleted bit NOT NULL,
	agt_date_deleted datetime2 NULL,
	isUpdateAfterActivation bit NULL,
	agt_action varchar(100) COLLATE French_CI_AS NULL,
	agt_parent_id int NULL
);


-- referentiel_fudpe_new.dbo.agent_bkp2502025 definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.agent_bkp2502025;

CREATE TABLE referentiel_fudpe_new.dbo.agent_bkp2502025 (
	agt_id int IDENTITY(51101201,1) NOT NULL,
	agt_matricule_solde varchar(15) COLLATE French_CI_AS NULL,
	agt_cni varchar(25) COLLATE French_CI_AS NULL,
	agt_matricule_interne varchar(50) COLLATE French_CI_AS NULL,
	agt_prenom varchar(255) COLLATE French_CI_AS NULL,
	agt_nom varchar(255) COLLATE French_CI_AS NULL,
	agt_date_naissance date NULL,
	agt_lieu_naissance varchar(255) COLLATE French_CI_AS NULL,
	agt_adresse varchar(255) COLLATE French_CI_AS NULL,
	agt_genre varchar(5) COLLATE French_CI_AS NULL,
	agt_situation_matrimoniale varchar(50) COLLATE French_CI_AS NULL,
	agt_telephone varchar(15) COLLATE French_CI_AS NULL,
	agt_email varchar(255) COLLATE French_CI_AS NULL,
	agt_prenom_pere varchar(255) COLLATE French_CI_AS NULL,
	agt_prenom_mere varchar(255) COLLATE French_CI_AS NULL,
	agt_nom_mere varchar(255) COLLATE French_CI_AS NULL,
	agt_nb_enfants_charge int NULL,
	agt_date_derniere_situation date NULL,
	agt_date_derniere_position date NULL,
	agt_num_ordre varchar(255) COLLATE French_CI_AS NULL,
	agt_ref_syst_externe varchar(255) COLLATE French_CI_AS NULL,
	agt_ref_photo varchar(255) COLLATE French_CI_AS NULL,
	agt_cce_id int NULL,
	agt_pos_code varchar(3) COLLATE French_CI_AS NULL,
	agt_spe_code varchar(7) COLLATE French_CI_AS NULL,
	agt_affectation_id int NULL,
	agt_str_code varchar(20) COLLATE French_CI_AS NULL,
	agt_fct_code varchar(20) COLLATE French_CI_AS NULL,
	agt_user_id int NULL,
	agt_initiateur_id int NULL,
	agt_date_entree_service date NULL,
	agt_date_created datetime2 NULL,
	agt_date_updated datetime2 NULL,
	agt_ministere_code varchar(20) COLLATE French_CI_AS NULL,
	agt_deleted bit NOT NULL,
	agt_date_deleted datetime2 NULL,
	isUpdateAfterActivation bit NULL,
	agt_action varchar(100) COLLATE French_CI_AS NULL,
	agt_parent_id int NULL
);


-- referentiel_fudpe_new.dbo.agent_men_contractuels definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.agent_men_contractuels;

CREATE TABLE referentiel_fudpe_new.dbo.agent_men_contractuels (
	Matricule varchar(222) COLLATE French_CI_AS NULL,
	CNI varchar(222) COLLATE French_CI_AS NULL,
	Prénom varchar(222) COLLATE French_CI_AS NULL,
	Nom varchar(222) COLLATE French_CI_AS NULL,
	[Date de naissance] varchar(222) COLLATE French_CI_AS NULL,
	[Lieu de naissance] varchar(222) COLLATE French_CI_AS NULL,
	[Corps/Grade] varchar(222) COLLATE French_CI_AS NULL,
	téléphone varchar(222) COLLATE French_CI_AS NULL,
	Email varchar(222) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.agent_men_girafe_mat definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.agent_men_girafe_mat;

CREATE TABLE referentiel_fudpe_new.dbo.agent_men_girafe_mat (
	Matricule varchar(50) COLLATE French_CI_AS NULL,
	CNI varchar(50) COLLATE French_CI_AS NULL,
	Prénom varchar(50) COLLATE French_CI_AS NULL,
	Nom varchar(50) COLLATE French_CI_AS NULL,
	[Date de naissance] varchar(50) COLLATE French_CI_AS NULL,
	[Lieu de naissance] varchar(50) COLLATE French_CI_AS NULL,
	[Corps/Grade] varchar(50) COLLATE French_CI_AS NULL,
	téléphone int NULL,
	Email varchar(50) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.agent_men_match definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.agent_men_match;

CREATE TABLE referentiel_fudpe_new.dbo.agent_men_match (
	agt_id int IDENTITY(51101201,1) NOT NULL,
	agt_matricule_solde varchar(15) COLLATE French_CI_AS NULL,
	agt_cni varchar(25) COLLATE French_CI_AS NULL,
	agt_matricule_interne varchar(50) COLLATE French_CI_AS NULL,
	agt_prenom varchar(255) COLLATE French_CI_AS NULL,
	agt_nom varchar(255) COLLATE French_CI_AS NULL,
	agt_date_naissance date NULL,
	agt_lieu_naissance varchar(255) COLLATE French_CI_AS NULL,
	agt_adresse varchar(255) COLLATE French_CI_AS NULL,
	agt_genre varchar(5) COLLATE French_CI_AS NULL,
	agt_situation_matrimoniale varchar(50) COLLATE French_CI_AS NULL,
	agt_telephone varchar(15) COLLATE French_CI_AS NULL,
	agt_email varchar(255) COLLATE French_CI_AS NULL,
	agt_prenom_pere varchar(255) COLLATE French_CI_AS NULL,
	agt_prenom_mere varchar(255) COLLATE French_CI_AS NULL,
	agt_nom_mere varchar(255) COLLATE French_CI_AS NULL,
	agt_nb_enfants_charge int NULL,
	agt_date_derniere_situation date NULL,
	agt_date_derniere_position date NULL,
	agt_num_ordre varchar(255) COLLATE French_CI_AS NULL,
	agt_ref_syst_externe varchar(255) COLLATE French_CI_AS NULL,
	agt_ref_photo varchar(255) COLLATE French_CI_AS NULL,
	agt_cce_id int NULL,
	agt_pos_code varchar(3) COLLATE French_CI_AS NULL,
	agt_spe_code varchar(7) COLLATE French_CI_AS NULL,
	agt_affectation_id int NULL,
	agt_str_code varchar(20) COLLATE French_CI_AS NULL,
	agt_fct_code varchar(20) COLLATE French_CI_AS NULL,
	agt_user_id int NULL,
	agt_initiateur_id int NULL,
	agt_date_entree_service date NULL,
	agt_date_created datetime2 NULL,
	agt_date_updated datetime2 NULL,
	agt_ministere_code varchar(20) COLLATE French_CI_AS NULL,
	agt_deleted bit NOT NULL,
	agt_date_deleted datetime2 NULL,
	isUpdateAfterActivation bit NULL
);


-- referentiel_fudpe_new.dbo.agent_tmp05022024 definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.agent_tmp05022024;

CREATE TABLE referentiel_fudpe_new.dbo.agent_tmp05022024 (
	agt_id int IDENTITY(51101201,1) NOT NULL,
	agt_matricule_solde varchar(15) COLLATE French_CI_AS NULL,
	agt_cni varchar(25) COLLATE French_CI_AS NULL,
	agt_matricule_interne varchar(50) COLLATE French_CI_AS NULL,
	agt_prenom varchar(255) COLLATE French_CI_AS NULL,
	agt_nom varchar(255) COLLATE French_CI_AS NULL,
	agt_date_naissance date NULL,
	agt_lieu_naissance varchar(255) COLLATE French_CI_AS NULL,
	agt_adresse varchar(255) COLLATE French_CI_AS NULL,
	agt_genre varchar(5) COLLATE French_CI_AS NULL,
	agt_situation_matrimoniale varchar(50) COLLATE French_CI_AS NULL,
	agt_telephone varchar(15) COLLATE French_CI_AS NULL,
	agt_email varchar(255) COLLATE French_CI_AS NULL,
	agt_prenom_pere varchar(255) COLLATE French_CI_AS NULL,
	agt_prenom_mere varchar(255) COLLATE French_CI_AS NULL,
	agt_nom_mere varchar(255) COLLATE French_CI_AS NULL,
	agt_nb_enfants_charge int NULL,
	agt_date_derniere_situation date NULL,
	agt_date_derniere_position date NULL,
	agt_num_ordre varchar(255) COLLATE French_CI_AS NULL,
	agt_ref_syst_externe varchar(255) COLLATE French_CI_AS NULL,
	agt_ref_photo varchar(255) COLLATE French_CI_AS NULL,
	agt_cce_id int NULL,
	agt_pos_code varchar(3) COLLATE French_CI_AS NULL,
	agt_spe_code varchar(7) COLLATE French_CI_AS NULL,
	agt_affectation_id int NULL,
	agt_str_code varchar(20) COLLATE French_CI_AS NULL,
	agt_fct_code varchar(20) COLLATE French_CI_AS NULL,
	agt_user_id int NULL,
	agt_initiateur_id int NULL,
	agt_date_entree_service date NULL,
	agt_date_created datetime2 NULL,
	agt_date_updated datetime2 NULL,
	agt_ministere_code varchar(20) COLLATE French_CI_AS NULL,
	agt_deleted bit NOT NULL,
	agt_date_deleted datetime2 NULL,
	isUpdateAfterActivation bit NULL
);


-- referentiel_fudpe_new.dbo.agentmenactifs definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.agentmenactifs;

CREATE TABLE referentiel_fudpe_new.dbo.agentmenactifs (
	Matricule varchar(222) COLLATE French_CI_AS NULL,
	CNI varchar(222) COLLATE French_CI_AS NULL,
	Prénom varchar(222) COLLATE French_CI_AS NULL,
	Nom varchar(222) COLLATE French_CI_AS NULL,
	[Date de naissance] varchar(222) COLLATE French_CI_AS NULL,
	[Lieu de naissance] varchar(222) COLLATE French_CI_AS NULL,
	[Corps/Grade] varchar(222) COLLATE French_CI_AS NULL,
	téléphone varchar(222) COLLATE French_CI_AS NULL,
	Email varchar(222) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.agentsimplifie definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.agentsimplifie;

CREATE TABLE referentiel_fudpe_new.dbo.agentsimplifie (
	agt_id int NULL,
	agt_matricule_solde nvarchar(MAX) COLLATE French_CI_AS NULL,
	agt_cni nvarchar(MAX) COLLATE French_CI_AS NULL,
	agt_telephone nvarchar(MAX) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.armes_services definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.armes_services;

CREATE TABLE referentiel_fudpe_new.dbo.armes_services (
	arm_code nvarchar(10) COLLATE French_CI_AS NOT NULL,
	arm_description nvarchar(255) COLLATE French_CI_AS NULL,
	arm_libelle nvarchar(255) COLLATE French_CI_AS NULL,
	CONSTRAINT PK_armes_services PRIMARY KEY (arm_code)
);


-- referentiel_fudpe_new.dbo.bataillons definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.bataillons;

CREATE TABLE referentiel_fudpe_new.dbo.bataillons (
	code nvarchar(255) COLLATE French_CI_AS NOT NULL,
	libelle nvarchar(255) COLLATE French_CI_AS NULL,
	bat_ssec_code nvarchar(3) COLLATE French_CI_AS NULL,
	CONSTRAINT PK_bataillons PRIMARY KEY (code)
);


-- referentiel_fudpe_new.dbo.bordereau definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.bordereau;

CREATE TABLE referentiel_fudpe_new.dbo.bordereau (
	id int IDENTITY(1,1) NOT NULL,
	numero varchar(100) COLLATE French_CI_AS NOT NULL,
	datebordereau date NOT NULL,
	DATE_CREATION datetime DEFAULT getdate() NULL,
	DATE_UPDATED datetime DEFAULT getdate() NULL,
	DELETED bit DEFAULT 0 NULL,
	DATE_DELETED datetime NULL,
	bdr_structure varchar(20) COLLATE French_CI_AS NULL,
	code_type_acte varchar(100) COLLATE French_CI_AS NULL,
	CONSTRAINT PK__borderea__3213E83F963A00AA PRIMARY KEY (id)
);


-- referentiel_fudpe_new.dbo.categorie definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.categorie;

CREATE TABLE referentiel_fudpe_new.dbo.categorie (
	cat_code varchar(10) COLLATE French_CI_AS NOT NULL,
	cat_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK_categorie PRIMARY KEY (cat_code)
);


-- referentiel_fudpe_new.dbo.classe definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.classe;

CREATE TABLE referentiel_fudpe_new.dbo.classe (
	cls_code varchar(7) COLLATE French_CI_AS NOT NULL,
	cls_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	cls_description varchar(255) COLLATE French_CI_AS NULL,
	CONSTRAINT PK_classe PRIMARY KEY (cls_code)
);


-- referentiel_fudpe_new.dbo.college_groupes definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.college_groupes;

CREATE TABLE referentiel_fudpe_new.dbo.college_groupes (
	cg_clg_id bigint NOT NULL,
	cg_grp_id nvarchar(255) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK_college_groupes PRIMARY KEY (cg_clg_id,cg_grp_id)
);


-- referentiel_fudpe_new.dbo.colleges definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.colleges;

CREATE TABLE referentiel_fudpe_new.dbo.colleges (
	clg_id bigint NOT NULL,
	clg_code nvarchar(255) COLLATE French_CI_AS NULL,
	clg_description nvarchar(255) COLLATE French_CI_AS NULL,
	clg_libelle nvarchar(255) COLLATE French_CI_AS NULL,
	clg_cps_code nvarchar(7) COLLATE French_CI_AS NULL,
	clg_hier_id nvarchar(255) COLLATE French_CI_AS NULL,
	CONSTRAINT PK_colleges PRIMARY KEY (clg_id)
);


-- referentiel_fudpe_new.dbo.colleges_fonction definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.colleges_fonction;

CREATE TABLE referentiel_fudpe_new.dbo.colleges_fonction (
	cf_fctj_code nvarchar(7) COLLATE French_CI_AS NOT NULL,
	cf_clg_code bigint NOT NULL,
	CONSTRAINT PK_colleges_fonction PRIMARY KEY (cf_fctj_code,cf_clg_code)
);


-- referentiel_fudpe_new.dbo.configagentstructure definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.configagentstructure;

CREATE TABLE referentiel_fudpe_new.dbo.configagentstructure (
	CONFIG_DATE_CREATED datetime2 NULL,
	CONFIG_DATE_UPDATED datetime2 NULL,
	CODE_STRUCTURE varchar(100) COLLATE French_CI_AS NULL,
	CONFIG_ID int IDENTITY(1,1) NOT NULL,
	ID_ACCOUNT_AGENT int NOT NULL,
	CONSTRAINT configagentstructure_PK PRIMARY KEY (CONFIG_ID)
);


-- referentiel_fudpe_new.dbo.configurations definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.configurations;

CREATE TABLE referentiel_fudpe_new.dbo.configurations (
	config_id int NOT NULL,
	config_fieldid varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	config_fieldvalue varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	CONSTRAINT PK__configur__4AD1BFF18971780C PRIMARY KEY (config_id)
);


-- referentiel_fudpe_new.dbo.corps_classe_echelon_old definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.corps_classe_echelon_old;

CREATE TABLE referentiel_fudpe_new.dbo.corps_classe_echelon_old (
	cce_id int IDENTITY(1,1) NOT NULL,
	cce_cps_code varchar(10) COLLATE French_CI_AS NOT NULL,
	cce_cls_code varchar(7) COLLATE French_CI_AS NOT NULL,
	cce_ech_code varchar(7) COLLATE French_CI_AS NOT NULL,
	cce_duree int NOT NULL,
	cce_fin_grade bit NOT NULL,
	cce_fin_echelon bit NOT NULL,
	cce_operation char(1) COLLATE French_CI_AS NOT NULL,
	cce_appelation_grade varchar(255) COLLATE French_CI_AS NULL,
	cce_appelation_echelon varchar(255) COLLATE French_CI_AS NULL,
	cce_suivant int NULL,
	cce_fisrt bit NULL
);


-- referentiel_fudpe_new.dbo.delegation definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.delegation;

CREATE TABLE referentiel_fudpe_new.dbo.delegation (
	delegation_date_created datetime2 NULL,
	delegation_date_updated datetime2 NULL,
	id_account_agent int NULL,
	id_agent int NULL,
	nom_agent varchar(100) COLLATE French_CI_AS NULL,
	id_account_agent_delegate int NULL,
	id_agent_delegate int NULL,
	nom_agent_delegate varchar(100) COLLATE French_CI_AS NULL,
	code_structure varchar(100) COLLATE French_CI_AS NULL,
	code_fonction varchar(100) COLLATE French_CI_AS NULL,
	nom_structure varchar(100) COLLATE French_CI_AS NULL,
	nom_fonction varchar(100) COLLATE French_CI_AS NULL,
	etat bit NULL,
	delegation_id int IDENTITY(1,1) NOT NULL,
	user_id int NULL,
	CONSTRAINT delegation_PK PRIMARY KEY (delegation_id)
);


-- referentiel_fudpe_new.dbo.disciplines_enseignees definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.disciplines_enseignees;

CREATE TABLE referentiel_fudpe_new.dbo.disciplines_enseignees (
	de_id bigint NOT NULL,
	de_code nvarchar(10) COLLATE French_CI_AS NULL,
	description nvarchar(255) COLLATE French_CI_AS NULL,
	de_libelle nvarchar(255) COLLATE French_CI_AS NULL,
	CONSTRAINT PK_disciplines_enseignees PRIMARY KEY (de_id)
);


-- referentiel_fudpe_new.dbo.document_administratif definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.document_administratif;

CREATE TABLE referentiel_fudpe_new.dbo.document_administratif (
	doc_id int IDENTITY(1,1) NOT NULL,
	doc_date date DEFAULT NULL NULL,
	doc_description varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	doc_nature varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	doc_numauto varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	doc_objet varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	cheminDossier varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	doc_structure_origine varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	actif bit DEFAULT NULL NULL,
	doc_ministere_origine varchar(20) COLLATE French_CI_AS DEFAULT NULL NULL,
	chemin_dossier varchar(255) COLLATE French_CI_AS NULL,
	CONSTRAINT PK__document__8AD029245149495F PRIMARY KEY (doc_id)
);


-- referentiel_fudpe_new.dbo.echelon definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.echelon;

CREATE TABLE referentiel_fudpe_new.dbo.echelon (
	ech_code varchar(7) COLLATE French_CI_AS NOT NULL,
	ech_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	ech_description varchar(255) COLLATE French_CI_AS NULL,
	CONSTRAINT PK__echelon__C68B6C69ABA0E6E8 PRIMARY KEY (ech_code)
);


-- referentiel_fudpe_new.dbo.enseignant definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.enseignant;

CREATE TABLE referentiel_fudpe_new.dbo.enseignant (
	agt_id int IDENTITY(51101201,1) NOT NULL,
	agt_matricule_solde varchar(15) COLLATE French_CI_AS NULL,
	agt_cni varchar(25) COLLATE French_CI_AS NULL,
	agt_matricule_interne varchar(50) COLLATE French_CI_AS NULL,
	agt_prenom varchar(255) COLLATE French_CI_AS NULL,
	agt_nom varchar(255) COLLATE French_CI_AS NULL,
	agt_date_naissance date NULL,
	agt_lieu_naissance varchar(255) COLLATE French_CI_AS NULL,
	agt_adresse varchar(255) COLLATE French_CI_AS NULL,
	agt_genre varchar(5) COLLATE French_CI_AS NULL,
	agt_situation_matrimoniale varchar(50) COLLATE French_CI_AS NULL,
	agt_telephone varchar(15) COLLATE French_CI_AS NULL,
	agt_email varchar(255) COLLATE French_CI_AS NULL,
	agt_prenom_pere varchar(255) COLLATE French_CI_AS NULL,
	agt_prenom_mere varchar(255) COLLATE French_CI_AS NULL,
	agt_nom_mere varchar(255) COLLATE French_CI_AS NULL,
	agt_nb_enfants_charge int NULL,
	agt_date_derniere_situation date NULL,
	agt_date_derniere_position date NULL,
	agt_num_ordre varchar(255) COLLATE French_CI_AS NULL,
	agt_ref_syst_externe varchar(255) COLLATE French_CI_AS NULL,
	agt_ref_photo varchar(255) COLLATE French_CI_AS NULL,
	agt_cce_id int NULL,
	agt_pos_code varchar(3) COLLATE French_CI_AS NULL,
	agt_spe_code varchar(7) COLLATE French_CI_AS NULL,
	agt_affectation_id int NULL,
	agt_str_code varchar(20) COLLATE French_CI_AS NULL,
	agt_fct_code varchar(20) COLLATE French_CI_AS NULL,
	agt_user_id int NULL,
	agt_initiateur_id int NULL,
	agt_date_entree_service date NULL,
	agt_date_created datetime2 NULL,
	agt_date_updated datetime2 NULL,
	agt_ministere_code varchar(20) COLLATE French_CI_AS NULL,
	agt_deleted bit NOT NULL,
	agt_date_deleted datetime2 NULL,
	isUpdateAfterActivation bit NULL
);


-- referentiel_fudpe_new.dbo.erreur_numero_acte definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.erreur_numero_acte;

CREATE TABLE referentiel_fudpe_new.dbo.erreur_numero_acte (
	act_id int IDENTITY(50684612,1) NOT NULL,
	act_is_projet bit NOT NULL,
	act_numero_projet varchar(255) COLLATE French_CI_AS NULL,
	act_date_projet date NULL,
	act_numero_acte varchar(255) COLLATE French_CI_AS NULL,
	act_date_acte date NULL,
	act_observation varchar(255) COLLATE French_CI_AS NULL,
	act_ref_GED varchar(255) COLLATE French_CI_AS NULL,
	act_prise_en_compte_solde bit NOT NULL,
	act_ref_syst_externe varchar(255) COLLATE French_CI_AS NULL,
	act_tac_id int NOT NULL,
	act_act_lie int NULL,
	act_initiateur_id int NULL,
	act_process_instance_id int NULL,
	act_date_created datetime2 NULL,
	act_date_updated datetime2 NULL,
	act_deleted bit NOT NULL,
	act_date_deleted datetime2 NULL,
	act_etat_id int NULL,
	act_chemin_word varchar(255) COLLATE French_CI_AS NULL,
	act_numero_etape_circuit int NULL,
	act_str_parent_initiateur varchar(100) COLLATE French_CI_AS NULL,
	act_str_initiateur varchar(100) COLLATE French_CI_AS NULL,
	act_str_projet_acte varchar(100) COLLATE French_CI_AS NULL,
	act_is_rejet numeric(38,0) NULL,
	act_fonct_initiateur varchar(100) COLLATE French_CI_AS NULL,
	act_str_parent_projet_acte varchar(100) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.etat_acte definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.etat_acte;

CREATE TABLE referentiel_fudpe_new.dbo.etat_acte (
	eta_act_id int IDENTITY(1,1) NOT NULL,
	eta_act_code varchar(32) COLLATE French_CI_AS NOT NULL,
	eta_act_libelle varchar(255) COLLATE French_CI_AS NOT NULL,
	eta_act_is_rejete bit DEFAULT NULL NULL,
	eta_act_is_disponible bit DEFAULT NULL NULL,
	eta_act_structure_traitant varchar(100) COLLATE French_CI_AS NULL,
	eta_act_fonction_traitant varchar(100) COLLATE French_CI_AS NULL,
	CONSTRAINT PK_etat_acte PRIMARY KEY (eta_act_id),
	CONSTRAINT UC_etat_acte_code UNIQUE (eta_act_code)
);


-- referentiel_fudpe_new.dbo.etat_acte_action definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.etat_acte_action;

CREATE TABLE referentiel_fudpe_new.dbo.etat_acte_action (
	action_id int NOT NULL,
	eta_act_id int NOT NULL,
	CONSTRAINT PK_etat_acte_action PRIMARY KEY (action_id,eta_act_id)
);


-- referentiel_fudpe_new.dbo.etat_dossier definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.etat_dossier;

CREATE TABLE referentiel_fudpe_new.dbo.etat_dossier (
	id int IDENTITY(1,1) NOT NULL,
	code varchar(100) COLLATE French_CI_AS NOT NULL,
	libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	DATE_UPDATED datetime DEFAULT getdate() NULL,
	DELETED bit DEFAULT 0 NULL,
	DATE_DELETED datetime NULL,
	DATE_CREATION datetime NULL,
	CONSTRAINT PK__etat_dos__3213E83F5F2EE6C1 PRIMARY KEY (id)
);


-- referentiel_fudpe_new.dbo.etat_projet definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.etat_projet;

CREATE TABLE referentiel_fudpe_new.dbo.etat_projet (
	etp_id int IDENTITY(1,1) NOT NULL,
	etp_code varchar(50) COLLATE French_CI_AS NULL,
	etp_libelle varchar(100) COLLATE French_CI_AS NULL,
	CONSTRAINT PK_etat_projet PRIMARY KEY (etp_id)
);


-- referentiel_fudpe_new.dbo.fichier definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.fichier;

CREATE TABLE referentiel_fudpe_new.dbo.fichier (
	act_id bigint NULL,
	chemin varchar(255) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.genre definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.genre;

CREATE TABLE referentiel_fudpe_new.dbo.genre (
	code varchar(10) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK_genre PRIMARY KEY (code)
);


-- referentiel_fudpe_new.dbo.grands_services_commandements definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.grands_services_commandements;

CREATE TABLE referentiel_fudpe_new.dbo.grands_services_commandements (
	id bigint NOT NULL,
	libelle nvarchar(255) COLLATE French_CI_AS NULL,
	CONSTRAINT PK_grands_services_commandements PRIMARY KEY (id)
);


-- referentiel_fudpe_new.dbo.groupe_classes definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.groupe_classes;

CREATE TABLE referentiel_fudpe_new.dbo.groupe_classes (
	gc_grp_id nvarchar(255) COLLATE French_CI_AS NOT NULL,
	gc_cls_id nvarchar(7) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK_groupe_classes PRIMARY KEY (gc_grp_id,gc_cls_id)
);


-- referentiel_fudpe_new.dbo.groupe_echelons definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.groupe_echelons;

CREATE TABLE referentiel_fudpe_new.dbo.groupe_echelons (
	ge_grp_id nvarchar(255) COLLATE French_CI_AS NOT NULL,
	ge_ech_id nvarchar(7) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK_groupe_echelons PRIMARY KEY (ge_grp_id,ge_ech_id)
);


-- referentiel_fudpe_new.dbo.groupe_fonctions definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.groupe_fonctions;

CREATE TABLE referentiel_fudpe_new.dbo.groupe_fonctions (
	gf_grp_id nvarchar(255) COLLATE French_CI_AS NOT NULL,
	gf_fct_id nvarchar(7) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK_groupe_fonctions PRIMARY KEY (gf_grp_id,gf_fct_id)
);


-- referentiel_fudpe_new.dbo.groupes definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.groupes;

CREATE TABLE referentiel_fudpe_new.dbo.groupes (
	grp_code nvarchar(255) COLLATE French_CI_AS NOT NULL,
	grp_description nvarchar(255) COLLATE French_CI_AS NULL,
	grp_libelle nvarchar(255) COLLATE French_CI_AS NULL,
	grpe_hier_id nvarchar(255) COLLATE French_CI_AS NULL,
	CONSTRAINT PK_groupes PRIMARY KEY (grp_code)
);


-- referentiel_fudpe_new.dbo.hierarchie definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.hierarchie;

CREATE TABLE referentiel_fudpe_new.dbo.hierarchie (
	hier_code varchar(10) COLLATE French_CI_AS NOT NULL,
	hier_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	hier_description varchar(255) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK__hierarch__DE0EF1D6C6826CE1 PRIMARY KEY (hier_code)
);


-- referentiel_fudpe_new.dbo.historique_dossier_agent definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.historique_dossier_agent;

CREATE TABLE referentiel_fudpe_new.dbo.historique_dossier_agent (
	hist_da_id int IDENTITY(1,1) NOT NULL,
	hist_da_agt_id int NULL,
	hist_da_type_action varchar(100) COLLATE French_CI_AS NOT NULL,
	hist_da_libelle_action varchar(100) COLLATE French_CI_AS NOT NULL,
	hist_da_date_created datetime2 NOT NULL,
	hist_da_agt_name varchar(100) COLLATE French_CI_AS NULL,
	hist_da_agt_acteur_id int NULL,
	hist_da_agt_acteur_name varchar(100) COLLATE French_CI_AS NULL,
	CONSTRAINT historique_dossier_agent_PK PRIMARY KEY (hist_da_id)
);


-- referentiel_fudpe_new.dbo.historique_rejets definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.historique_rejets;

CREATE TABLE referentiel_fudpe_new.dbo.historique_rejets (
	id bigint IDENTITY(1,1) NOT NULL,
	hist_act_id bigint NOT NULL,
	hist_rejected_by varchar(100) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK__historiq__3213E83F32CBFD0E PRIMARY KEY (id)
);


-- referentiel_fudpe_new.dbo.historique_transaction_signature definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.historique_transaction_signature;

CREATE TABLE referentiel_fudpe_new.dbo.historique_transaction_signature (
	hta_id int IDENTITY(1,1) NOT NULL,
	hta_id_user_principal int DEFAULT NULL NULL,
	hta_id_user_sentrust varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	hta_token text COLLATE French_CI_AS DEFAULT NULL NULL,
	hta_date_created datetime DEFAULT NULL NULL,
	hta_date_updated datetime DEFAULT NULL NULL,
	hta_state varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	hta_eventInstanceName varchar(255) COLLATE French_CI_AS NULL,
	CONSTRAINT PK_historique_transaction_signature PRIMARY KEY (hta_id)
);


-- referentiel_fudpe_new.dbo.indemnite_retraite definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.indemnite_retraite;

CREATE TABLE referentiel_fudpe_new.dbo.indemnite_retraite (
	ind_ret_id int NOT NULL,
	int_ret_tranche_1 int NULL,
	ind_ret_date_debut_t1 date NULL,
	ind_ret_date_fin_t1 date NULL,
	int_ret_tranche_2 int NULL,
	ind_ret_date_debut_t2 date NULL,
	ind_ret_date_fin_t2 date NULL,
	int_ret_tranche_3 int NULL,
	ind_ret_date_debut_t3 date NULL,
	ind_ret_date_fin_t3 date NULL,
	CONSTRAINT PK__indemnit__6586C93E56AF169A PRIMARY KEY (ind_ret_id)
);


-- referentiel_fudpe_new.dbo.interface_solde definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.interface_solde;

CREATE TABLE referentiel_fudpe_new.dbo.interface_solde (
	id int IDENTITY(1,1) NOT NULL,
	matricule_solde varchar(20) COLLATE French_CI_AS NOT NULL,
	cni varchar(15) COLLATE French_CI_AS NOT NULL,
	critere varchar(255) COLLATE French_CI_AS NOT NULL,
	ancienne_valeur varchar(255) COLLATE French_CI_AS NOT NULL,
	nouvelle_valeur varchar(255) COLLATE French_CI_AS NOT NULL,
	date_acte date NOT NULL,
	numero_acte varchar(255) COLLATE French_CI_AS NOT NULL,
	ref_GED varchar(255) COLLATE French_CI_AS NOT NULL,
	date_effet_acte date NOT NULL,
	type_acte varchar(255) COLLATE French_CI_AS NOT NULL,
	date_reception date NOT NULL,
	date_maj date NOT NULL,
	motif_rejet varchar(255) COLLATE French_CI_AS NOT NULL,
	prise_en_compte_matricule varchar(255) COLLATE French_CI_AS NOT NULL,
	code_retour varchar(255) COLLATE French_CI_AS NOT NULL,
	etat varchar(20) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK_interface_solde PRIMARY KEY (id)
);


-- referentiel_fudpe_new.dbo.legions definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.legions;

CREATE TABLE referentiel_fudpe_new.dbo.legions (
	code nvarchar(255) COLLATE French_CI_AS NOT NULL,
	libelle nvarchar(255) COLLATE French_CI_AS NULL,
	leg_ssec_code nvarchar(3) COLLATE French_CI_AS NULL,
	CONSTRAINT PK_legions PRIMARY KEY (code)
);


-- referentiel_fudpe_new.dbo.lieux_naissance definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.lieux_naissance;

CREATE TABLE referentiel_fudpe_new.dbo.lieux_naissance (
	lieu_code nvarchar(15) COLLATE French_CI_AS NOT NULL,
	lieu_libelle nvarchar(255) COLLATE French_CI_AS NULL,
	CONSTRAINT PK_lieux_naissance PRIMARY KEY (lieu_code)
);


-- referentiel_fudpe_new.dbo.matricule definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.matricule;

CREATE TABLE referentiel_fudpe_new.dbo.matricule (
	agt_id int NULL,
	agt_matricule_solde nvarchar(MAX) COLLATE French_CI_AS NULL,
	agt_cni nvarchar(MAX) COLLATE French_CI_AS NULL,
	agt_telephone nvarchar(MAX) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.matriculeinterne definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.matriculeinterne;

CREATE TABLE referentiel_fudpe_new.dbo.matriculeinterne (
	agt_id int NULL,
	agt_matricule_solde nvarchar(MAX) COLLATE French_CI_AS NULL,
	agt_cni nvarchar(MAX) COLLATE French_CI_AS NULL,
	agt_telephone nvarchar(MAX) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.parametrage_template_acte_bkp definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.parametrage_template_acte_bkp;

CREATE TABLE referentiel_fudpe_new.dbo.parametrage_template_acte_bkp (
	id int NOT NULL,
	is_individuel bit NOT NULL,
	nature varchar(50) COLLATE French_CI_AS NULL,
	type_corps varchar(15) COLLATE French_CI_AS NULL,
	ref_model varchar(255) COLLATE French_CI_AS NULL,
	sous_secteur varchar(7) COLLATE French_CI_AS NULL,
	type_acte int NOT NULL,
	json_data varchar(1500) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.parametres_supplementaires definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.parametres_supplementaires;

CREATE TABLE referentiel_fudpe_new.dbo.parametres_supplementaires (
	param_gen_id int IDENTITY(1,1) NOT NULL,
	param_gen_code varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	param_gen_valeur varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	CONSTRAINT PK__parametr__93991B8B2118124A PRIMARY KEY (param_gen_id)
);


-- referentiel_fudpe_new.dbo.pays definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.pays;

CREATE TABLE referentiel_fudpe_new.dbo.pays (
	PAYS_ID int IDENTITY(1,1) NOT NULL,
	PAYS_NAME varchar(80) COLLATE French_CI_AS NOT NULL,
	PAYS_CODE char(2) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK__pays__9C401D82D6B990FE PRIMARY KEY (PAYS_ID)
);


-- referentiel_fudpe_new.dbo.pieces_jointes definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.pieces_jointes;

CREATE TABLE referentiel_fudpe_new.dbo.pieces_jointes (
	id bigint NULL,
	chemin varchar(255) COLLATE French_CI_AS NULL,
	reference varchar(255) COLLATE French_CI_AS NULL,
	agent_agt_id bigint NULL,
	type_code varchar(255) COLLATE French_CI_AS NULL,
	dateActe datetime2 NULL,
	dateEffet datetime2 NULL,
	numeroActe varchar(255) COLLATE French_CI_AS NULL,
	statut int NOT NULL,
	act_tac_code bigint NULL
);


-- referentiel_fudpe_new.dbo.reference definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.reference;

CREATE TABLE referentiel_fudpe_new.dbo.reference (
	ref_id int IDENTITY(1,1) NOT NULL,
	ref_description varchar(4000) COLLATE French_CI_AS NOT NULL,
	ref_lienFichier varchar(4000) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK__referenc__BDA5A86980791DA4 PRIMARY KEY (ref_id)
);


-- referentiel_fudpe_new.dbo.reservations_numeros definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.reservations_numeros;

CREATE TABLE referentiel_fudpe_new.dbo.reservations_numeros (
	res_id int IDENTITY(1,1) NOT NULL,
	res_date date DEFAULT NULL NULL,
	res_description varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	res_from int DEFAULT NULL NULL,
	res_value int DEFAULT NULL NULL,
	res_nature varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	CONSTRAINT PK__reservat__2090B50D92BF238E PRIMARY KEY (res_id)
);


-- referentiel_fudpe_new.dbo.reservations_numeros_bkp definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.reservations_numeros_bkp;

CREATE TABLE referentiel_fudpe_new.dbo.reservations_numeros_bkp (
	res_id int NOT NULL,
	res_date date NULL,
	res_description varchar(255) COLLATE French_CI_AS NULL,
	res_from int NULL,
	res_value int NULL,
	res_nature varchar(255) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.retraite_src_dpr definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.retraite_src_dpr;

CREATE TABLE referentiel_fudpe_new.dbo.retraite_src_dpr (
	Matricule varchar(50) COLLATE French_CI_AS NULL,
	Prénom varchar(50) COLLATE French_CI_AS NULL,
	Nom varchar(50) COLLATE French_CI_AS NULL,
	Date_naissance varchar(50) COLLATE French_CI_AS NULL,
	Corps varchar(50) COLLATE French_CI_AS NULL,
	[Position] varchar(50) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.secteur definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.secteur;

CREATE TABLE referentiel_fudpe_new.dbo.secteur (
	sec_code varchar(5) COLLATE French_CI_AS NOT NULL,
	sec_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	sec_description varchar(255) COLLATE French_CI_AS NULL,
	CONSTRAINT PK__secteur__9B822886E7EDE323 PRIMARY KEY (sec_code)
);


-- referentiel_fudpe_new.dbo.soldeAgent definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.soldeAgent;

CREATE TABLE referentiel_fudpe_new.dbo.soldeAgent (
	COD_EMPL varchar(5000) COLLATE French_CI_AS NULL,
	PRE_EMPL varchar(5000) COLLATE French_CI_AS NULL,
	NOM_EMPL varchar(5000) COLLATE French_CI_AS NULL,
	DAT_NAI_EMPL varchar(5000) COLLATE French_CI_AS NULL,
	NUM_PIE_IDE_EMPL varchar(5000) COLLATE French_CI_AS NULL,
	SEX_EMPL varchar(5000) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.specialite definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.specialite;

CREATE TABLE referentiel_fudpe_new.dbo.specialite (
	spe_code varchar(7) COLLATE French_CI_AS NOT NULL,
	spe_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	spe_description varchar(255) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK__speciali__6B470C85B4FCF9EE PRIMARY KEY (spe_code)
);


-- referentiel_fudpe_new.dbo.statistiques_corps definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.statistiques_corps;

CREATE TABLE referentiel_fudpe_new.dbo.statistiques_corps (
	id int IDENTITY(1,1) NOT NULL,
	codeCadre varchar(50) COLLATE French_CI_AS NULL,
	codeCorps varchar(50) COLLATE French_CI_AS NULL,
	libCorps varchar(255) COLLATE French_CI_AS NULL,
	total int NULL
);


-- referentiel_fudpe_new.dbo.statistiques_corps_genre definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.statistiques_corps_genre;

CREATE TABLE referentiel_fudpe_new.dbo.statistiques_corps_genre (
	id int IDENTITY(1,1) NOT NULL,
	codeCadre varchar(50) COLLATE French_CI_AS NULL,
	codeCorps varchar(50) COLLATE French_CI_AS NULL,
	libCorps varchar(255) COLLATE French_CI_AS NULL,
	genre varchar(5) COLLATE French_CI_AS NULL,
	total int NULL
);


-- referentiel_fudpe_new.dbo.statistiques_hierarchie_genre definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.statistiques_hierarchie_genre;

CREATE TABLE referentiel_fudpe_new.dbo.statistiques_hierarchie_genre (
	id int IDENTITY(1,1) NOT NULL,
	codeCadre varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	codeHier varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	libHier varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	genre varchar(5) COLLATE French_CI_AS DEFAULT NULL NULL,
	total int DEFAULT NULL NULL
);


-- referentiel_fudpe_new.dbo.statistiques_position definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.statistiques_position;

CREATE TABLE referentiel_fudpe_new.dbo.statistiques_position (
	id int IDENTITY(1,1) NOT NULL,
	codecorps varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	codePos varchar(5) COLLATE French_CI_AS DEFAULT NULL NULL,
	libPos varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	total int DEFAULT NULL NULL
);


-- referentiel_fudpe_new.dbo.statistiques_previsions_avancements definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.statistiques_previsions_avancements;

CREATE TABLE referentiel_fudpe_new.dbo.statistiques_previsions_avancements (
	id int IDENTITY(1,1) NOT NULL,
	agtId int NOT NULL,
	matricule varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	prenom varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	nom varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	dateNaissance date DEFAULT NULL NULL,
	codeCorps varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	libCorps varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	codeClasse varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	libClasse varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	codeEchelon varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	libEchelon varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	dateDerniereSituation date DEFAULT NULL NULL,
	ancieneteRequise int DEFAULT NULL NULL,
	finGrade bit DEFAULT NULL NULL,
	cceId int DEFAULT NULL NULL,
	idTypeActe int NULL
);


-- referentiel_fudpe_new.dbo.statistiques_projet_acte definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.statistiques_projet_acte;

CREATE TABLE referentiel_fudpe_new.dbo.statistiques_projet_acte (
	id int IDENTITY(1,1) NOT NULL,
	idEtat int NULL,
	libEtat varchar(255) COLLATE French_CI_AS NULL,
	idActeur int NULL,
	libActeur varchar(255) COLLATE French_CI_AS NULL,
	total int NULL,
	CONSTRAINT PK__statisti__3213E83F3B4997F1 PRIMARY KEY (id)
);
 CREATE NONCLUSTERED INDEX Statistiques_ProjetActe_idActeur ON referentiel_fudpe_new.dbo.statistiques_projet_acte (  idActeur ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;
 CREATE NONCLUSTERED INDEX Statistiques_Projet_idEtat ON referentiel_fudpe_new.dbo.statistiques_projet_acte (  idEtat ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;


-- referentiel_fudpe_new.dbo.statistiques_pyramide_age definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.statistiques_pyramide_age;

CREATE TABLE referentiel_fudpe_new.dbo.statistiques_pyramide_age (
	id int IDENTITY(1,1) NOT NULL,
	codeCorps varchar(50) COLLATE French_CI_AS NULL,
	plageAge varchar(15) COLLATE French_CI_AS NULL,
	total int NULL,
	CONSTRAINT PK_statistiques_pyramide_age PRIMARY KEY (id)
);


-- referentiel_fudpe_new.dbo.statistiques_retraites_annee_courante definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.statistiques_retraites_annee_courante;

CREATE TABLE referentiel_fudpe_new.dbo.statistiques_retraites_annee_courante (
	id int IDENTITY(1,1) NOT NULL,
	agtId int NOT NULL,
	matricule varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	prenom varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	nom varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	dateNaissance date DEFAULT NULL NULL,
	codeCorps varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	libCorps varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	codeClasse varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	libClasse varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	codeEchelon varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	libEchelon varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	idTypeActe int NULL,
	[INSERT INTO [SELECT a.agt_id] varchar(129) COLLATE French_CI_AS NULL,
	[a.agt_matricule_solde] varchar(26) COLLATE French_CI_AS NULL,
	[ a.agt_prenom] varchar(30) COLLATE French_CI_AS NULL,
	[ a.agt_nom] varchar(37) COLLATE French_CI_AS NULL,
	[a.agt_date_naissance] varchar(20) COLLATE French_CI_AS NULL,
	[ co.cps_code] varchar(42) COLLATE French_CI_AS NULL,
	[ co.cps_libelle] varchar(18) COLLATE French_CI_AS NULL,
	[cl.cls_code] varchar(38) COLLATE French_CI_AS NULL,
	[ cl.cls_libelle] varchar(15) COLLATE French_CI_AS NULL,
	[ec.ech_code] varchar(17) COLLATE French_CI_AS NULL,
	[ ec.ech_libelle] varchar(15) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.statistiques_retraites_annee_prochaine definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.statistiques_retraites_annee_prochaine;

CREATE TABLE referentiel_fudpe_new.dbo.statistiques_retraites_annee_prochaine (
	id int IDENTITY(1,1) NOT NULL,
	agtId int NOT NULL,
	matricule varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	prenom varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	nom varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	dateNaissance date DEFAULT NULL NULL,
	codeCorps varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	libCorps varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	codeClasse varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	libClasse varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	codeEchelon varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	libEchelon varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL
);


-- referentiel_fudpe_new.dbo.statut_signature definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.statut_signature;

CREATE TABLE referentiel_fudpe_new.dbo.statut_signature (
	code varchar(10) COLLATE French_CI_AS NOT NULL,
	satut varchar(50) COLLATE French_CI_AS DEFAULT NULL NULL,
	id int DEFAULT 0 NOT NULL
);


-- referentiel_fudpe_new.dbo.structure_bkp30042024 definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.structure_bkp30042024;

CREATE TABLE referentiel_fudpe_new.dbo.structure_bkp30042024 (
	str_code varchar(20) COLLATE French_CI_AS NULL,
	str_libelle varchar(255) COLLATE French_CI_AS NULL,
	str_description varchar(255) COLLATE French_CI_AS NULL,
	str_type_code varchar(10) COLLATE French_CI_AS NULL,
	str_parent_code varchar(20) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.table_correspondance definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.table_correspondance;

CREATE TABLE referentiel_fudpe_new.dbo.table_correspondance (
	id int NULL,
	DATE_CREATION datetime NULL,
	DATE_UPDATED datetime NULL,
	DELETED bit NULL,
	DATE_DELETED datetime NULL,
	bdr_structure varchar(255) COLLATE French_CI_AS NULL,
	bdr_typeacte int NULL,
	code_corps varchar(100) COLLATE French_CI_AS NULL,
	bdr_code_typeacte varchar(255) COLLATE French_CI_AS NULL
);


-- referentiel_fudpe_new.dbo.type_corps definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.type_corps;

CREATE TABLE referentiel_fudpe_new.dbo.type_corps (
	typc_code varchar(15) COLLATE French_CI_AS NOT NULL,
	typc_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK__typecorp__06C0DEAA81CE4D4D PRIMARY KEY (typc_code)
);


-- referentiel_fudpe_new.dbo.type_des definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.type_des;

CREATE TABLE referentiel_fudpe_new.dbo.type_des (
	id int IDENTITY(1,1) NOT NULL,
	des_libelle varchar(255) COLLATE French_CI_AS NULL,
	DATE_CREATION datetime DEFAULT getdate() NULL,
	DATE_UPDATED datetime DEFAULT getdate() NULL,
	DELETED bit DEFAULT 0 NULL,
	DATE_DELETED datetime NULL,
	CONSTRAINT type_des_PK PRIMARY KEY (id)
);


-- referentiel_fudpe_new.dbo.type_diplome definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.type_diplome;

CREATE TABLE referentiel_fudpe_new.dbo.type_diplome (
	typdpl_code varchar(10) COLLATE French_CI_AS NOT NULL,
	typdpl_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK_type_diplome PRIMARY KEY (typdpl_code)
);


-- referentiel_fudpe_new.dbo.type_position definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.type_position;

CREATE TABLE referentiel_fudpe_new.dbo.type_position (
	typos_code varchar(30) COLLATE French_CI_AS NOT NULL,
	typos_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK_type_position PRIMARY KEY (typos_code)
);


-- referentiel_fudpe_new.dbo.type_sanction definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.type_sanction;

CREATE TABLE referentiel_fudpe_new.dbo.type_sanction (
	tpsanc_id int IDENTITY(1,1) NOT NULL,
	tpsanc_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	tpsanc_duree int NOT NULL,
	tpsanc_nbRenouvellement int NOT NULL,
	CONSTRAINT PK__typesanc__C4497F18D479E769 PRIMARY KEY (tpsanc_id)
);


-- referentiel_fudpe_new.dbo.unites definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.unites;

CREATE TABLE referentiel_fudpe_new.dbo.unites (
	unit_code nvarchar(10) COLLATE French_CI_AS NOT NULL,
	unit_description nvarchar(255) COLLATE French_CI_AS NULL,
	unit_libelle nvarchar(255) COLLATE French_CI_AS NULL,
	unit_str_code nvarchar(10) COLLATE French_CI_AS NULL,
	unit_ssec_code nvarchar(3) COLLATE French_CI_AS NULL,
	CONSTRAINT PK_unites PRIMARY KEY (unit_code)
);


-- referentiel_fudpe_new.dbo.diplome definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.diplome;

CREATE TABLE referentiel_fudpe_new.dbo.diplome (
	dip_code varchar(10) COLLATE French_CI_AS NOT NULL,
	dip_libelle varchar(255) COLLATE French_CI_AS NOT NULL,
	dip_description varchar(255) COLLATE French_CI_AS NULL,
	dip_typdpl_code varchar(10) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK__diplome__6BF8517BEA23C25A PRIMARY KEY (dip_code),
	CONSTRAINT FK_diplome_type_diplome FOREIGN KEY (dip_typdpl_code) REFERENCES referentiel_fudpe_new.dbo.type_diplome(typdpl_code)
);


-- referentiel_fudpe_new.dbo.fonction definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.fonction;

CREATE TABLE referentiel_fudpe_new.dbo.fonction (
	fct_code varchar(20) COLLATE French_CI_AS NOT NULL,
	fct_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	fct_description varchar(255) COLLATE French_CI_AS NOT NULL,
	fct_superieur_code varchar(20) COLLATE French_CI_AS NULL,
	show bit NULL,
	CONSTRAINT PK__fonction__F89F7988ADA5F97D PRIMARY KEY (fct_code),
	CONSTRAINT FK_fonction_fonction FOREIGN KEY (fct_superieur_code) REFERENCES referentiel_fudpe_new.dbo.fonction(fct_code)
);
 CREATE NONCLUSTERED INDEX FCT_CODE_INDEX ON referentiel_fudpe_new.dbo.fonction (  fct_code ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;


-- referentiel_fudpe_new.dbo.[position] definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.[position];

CREATE TABLE referentiel_fudpe_new.dbo.[position] (
	pos_code varchar(3) COLLATE French_CI_AS NOT NULL,
	pos_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	pos_description varchar(255) COLLATE French_CI_AS NULL,
	pos_type_position_code varchar(30) COLLATE French_CI_AS NULL,
	CONSTRAINT PK__position__15CE528F6AE21522 PRIMARY KEY (pos_code),
	CONSTRAINT FK_position_type_position FOREIGN KEY (pos_type_position_code) REFERENCES referentiel_fudpe_new.dbo.type_position(typos_code)
);


-- referentiel_fudpe_new.dbo.sous_secteur definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.sous_secteur;

CREATE TABLE referentiel_fudpe_new.dbo.sous_secteur (
	ssec_code varchar(7) COLLATE French_CI_AS NOT NULL,
	ssec_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	ssec_description varchar(255) COLLATE French_CI_AS NULL,
	ssec_secteur_code varchar(5) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK__soussect__44469758C8CFBE1C PRIMARY KEY (ssec_code),
	CONSTRAINT FK_sous_secteur_secteur FOREIGN KEY (ssec_secteur_code) REFERENCES referentiel_fudpe_new.dbo.secteur(sec_code)
);


-- referentiel_fudpe_new.dbo.type_acte definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.type_acte;

CREATE TABLE referentiel_fudpe_new.dbo.type_acte (
	tac_id int IDENTITY(201,1) NOT NULL,
	tac_code varchar(10) COLLATE French_CI_AS NULL,
	tac_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	tac_description varchar(255) COLLATE French_CI_AS NOT NULL,
	tac_categorie_code varchar(10) COLLATE French_CI_AS NOT NULL,
	tac_secteur_code varchar(5) COLLATE French_CI_AS NULL,
	tac_chemin_form varchar(255) COLLATE French_CI_AS NULL,
	CONSTRAINT PK__typeacte__6A74B049F5982360 PRIMARY KEY (tac_id),
	CONSTRAINT FK_type_acte_categorie FOREIGN KEY (tac_categorie_code) REFERENCES referentiel_fudpe_new.dbo.categorie(cat_code),
	CONSTRAINT FK_type_acte_secteur FOREIGN KEY (tac_secteur_code) REFERENCES referentiel_fudpe_new.dbo.secteur(sec_code)
);
 CREATE NONCLUSTERED INDEX type_acte_code ON referentiel_fudpe_new.dbo.type_acte (  tac_code ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;
 CREATE NONCLUSTERED INDEX type_acte_secteur_code ON referentiel_fudpe_new.dbo.type_acte (  tac_secteur_code ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;


-- referentiel_fudpe_new.dbo.type_rejet definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.type_rejet;

CREATE TABLE referentiel_fudpe_new.dbo.type_rejet (
	code varchar(100) COLLATE French_CI_AS NOT NULL,
	libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	dos_type_act int NOT NULL,
	id int IDENTITY(1,1) NOT NULL,
	DATE_CREATION datetime NULL,
	DATE_UPDATED datetime NULL,
	DATE_DELETED datetime NULL,
	DELETED bit NULL,
	CONSTRAINT FK_type_rejet_type_acte FOREIGN KEY (dos_type_act) REFERENCES referentiel_fudpe_new.dbo.type_acte(tac_id)
);


-- referentiel_fudpe_new.dbo.type_sortie_temporaire definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.type_sortie_temporaire;

CREATE TABLE referentiel_fudpe_new.dbo.type_sortie_temporaire (
	tst_id int IDENTITY(1,1) NOT NULL,
	tst_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	tst_duree int NOT NULL,
	tst_nb_renouvellement int NOT NULL,
	tst_tac_id int NULL,
	CONSTRAINT PK__typesort__A92C56A762BABFEA PRIMARY KEY (tst_id),
	CONSTRAINT FK_type_sortie_temporaire_type_acte FOREIGN KEY (tst_tac_id) REFERENCES referentiel_fudpe_new.dbo.type_acte(tac_id)
);


-- referentiel_fudpe_new.dbo.type_structure definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.type_structure;

CREATE TABLE referentiel_fudpe_new.dbo.type_structure (
	typst_code varchar(10) COLLATE French_CI_AS NOT NULL,
	typst_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	typst_parent_code varchar(10) COLLATE French_CI_AS NULL,
	CONSTRAINT PK_type_structure PRIMARY KEY (typst_code),
	CONSTRAINT FK_type_structure_type_structure FOREIGN KEY (typst_parent_code) REFERENCES referentiel_fudpe_new.dbo.type_structure(typst_code)
);


-- referentiel_fudpe_new.dbo.acte definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.acte;

CREATE TABLE referentiel_fudpe_new.dbo.acte (
	act_id int IDENTITY(50684612,1) NOT NULL,
	act_is_projet bit NOT NULL,
	act_numero_projet varchar(255) COLLATE French_CI_AS NULL,
	act_date_projet date NULL,
	act_numero_acte varchar(255) COLLATE French_CI_AS NULL,
	act_date_acte date NULL,
	act_observation varchar(255) COLLATE French_CI_AS NULL,
	act_ref_GED varchar(255) COLLATE French_CI_AS NULL,
	act_prise_en_compte_solde bit NOT NULL,
	act_ref_syst_externe varchar(255) COLLATE French_CI_AS NULL,
	act_tac_id int NOT NULL,
	act_act_lie int NULL,
	act_initiateur_id int NULL,
	act_process_instance_id int NULL,
	act_date_created datetime2 NULL,
	act_date_updated datetime2 NULL,
	act_deleted bit DEFAULT 0 NOT NULL,
	act_date_deleted datetime2 NULL,
	act_etat_id int NULL,
	act_chemin_word varchar(255) COLLATE French_CI_AS NULL,
	act_numero_etape_circuit int NULL,
	act_str_parent_initiateur varchar(100) COLLATE French_CI_AS NULL,
	act_str_initiateur varchar(100) COLLATE French_CI_AS NULL,
	act_str_projet_acte varchar(100) COLLATE French_CI_AS NULL,
	act_is_rejet numeric(38,0) NULL,
	act_fonct_initiateur varchar(100) COLLATE French_CI_AS NULL,
	act_str_parent_projet_acte varchar(100) COLLATE French_CI_AS NULL,
	act_nbre_page int NULL,
	CONSTRAINT PK__acte__EBC8309582B3719C PRIMARY KEY (act_id),
	CONSTRAINT FK_acte_acte_lie FOREIGN KEY (act_act_lie) REFERENCES referentiel_fudpe_new.dbo.acte(act_id),
	CONSTRAINT FK_acte_etat_acte FOREIGN KEY (act_etat_id) REFERENCES referentiel_fudpe_new.dbo.etat_acte(eta_act_id),
	CONSTRAINT FK_acte_type_acte FOREIGN KEY (act_tac_id) REFERENCES referentiel_fudpe_new.dbo.type_acte(tac_id)
);
 CREATE NONCLUSTERED INDEX act_numero_acte ON referentiel_fudpe_new.dbo.acte (  act_numero_acte ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [ACTE ] ;
 CREATE NONCLUSTERED INDEX act_numero_projet ON referentiel_fudpe_new.dbo.acte (  act_numero_projet ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [ACTE ] ;
 CREATE NONCLUSTERED INDEX acte_act_etat_id ON referentiel_fudpe_new.dbo.acte (  act_etat_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [ACTE ] ;
 CREATE NONCLUSTERED INDEX acte_act_initiateur_id_idx ON referentiel_fudpe_new.dbo.acte (  act_initiateur_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [ACTE ] ;
 CREATE NONCLUSTERED INDEX acte_tac_id ON referentiel_fudpe_new.dbo.acte (  act_tac_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [ACTE ] ;


-- referentiel_fudpe_new.dbo.cadre definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.cadre;

CREATE TABLE referentiel_fudpe_new.dbo.cadre (
	cad_code varchar(10) COLLATE French_CI_AS NOT NULL,
	cad_libelle varchar(100) COLLATE French_CI_AS NOT NULL,
	cad_description varchar(255) COLLATE French_CI_AS NULL,
	cad_sous_secteur varchar(7) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK__cadre__B6910BDD6DD01C7D PRIMARY KEY (cad_code),
	CONSTRAINT FK_cadre_sous_secteur FOREIGN KEY (cad_sous_secteur) REFERENCES referentiel_fudpe_new.dbo.sous_secteur(ssec_code)
);
 CREATE NONCLUSTERED INDEX cad_sous_secteur ON referentiel_fudpe_new.dbo.cadre (  cad_sous_secteur ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;


-- referentiel_fudpe_new.dbo.corps definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.corps;

CREATE TABLE referentiel_fudpe_new.dbo.corps (
	cps_code varchar(10) COLLATE French_CI_AS NOT NULL,
	cps_libelle varchar(255) COLLATE French_CI_AS NOT NULL,
	cps_age_retraite int NOT NULL,
	cps_description varchar(255) COLLATE French_CI_AS NULL,
	cps_hierarchie_code varchar(10) COLLATE French_CI_AS NULL,
	cps_cadre_code varchar(10) COLLATE French_CI_AS NULL,
	cps_typecorps_code varchar(15) COLLATE French_CI_AS NULL,
	cps_libelle_singulier varchar(255) COLLATE French_CI_AS NULL,
	CONSTRAINT PK__corps__62D14947484DB48F PRIMARY KEY (cps_code),
	CONSTRAINT FK_corps_cadre FOREIGN KEY (cps_cadre_code) REFERENCES referentiel_fudpe_new.dbo.cadre(cad_code),
	CONSTRAINT FK_corps_hierarchie FOREIGN KEY (cps_hierarchie_code) REFERENCES referentiel_fudpe_new.dbo.hierarchie(hier_code),
	CONSTRAINT FK_corps_type_corps FOREIGN KEY (cps_typecorps_code) REFERENCES referentiel_fudpe_new.dbo.type_corps(typc_code)
);
 CREATE NONCLUSTERED INDEX corps_cadre_code ON referentiel_fudpe_new.dbo.corps (  cps_cadre_code ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;
 CREATE NONCLUSTERED INDEX corps_hierarchie_code ON referentiel_fudpe_new.dbo.corps (  cps_hierarchie_code ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;
 CREATE NONCLUSTERED INDEX corps_typecorps_code ON referentiel_fudpe_new.dbo.corps (  cps_typecorps_code ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;


-- referentiel_fudpe_new.dbo.corps_classe_echelon definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.corps_classe_echelon;

CREATE TABLE referentiel_fudpe_new.dbo.corps_classe_echelon (
	cce_id int IDENTITY(1,1) NOT NULL,
	cce_cps_code varchar(10) COLLATE French_CI_AS NOT NULL,
	cce_cls_code varchar(7) COLLATE French_CI_AS NOT NULL,
	cce_ech_code varchar(7) COLLATE French_CI_AS NOT NULL,
	cce_duree int NOT NULL,
	cce_fin_grade bit NOT NULL,
	cce_fin_echelon bit NOT NULL,
	cce_operation char(1) COLLATE French_CI_AS DEFAULT '=' NOT NULL,
	cce_appelation_grade varchar(255) COLLATE French_CI_AS NULL,
	cce_appelation_echelon varchar(255) COLLATE French_CI_AS NULL,
	cce_suivant int NULL,
	cce_fisrt bit NULL,
	CONSTRAINT PK__corps_cl__456535AD31F70BFC PRIMARY KEY (cce_id),
	CONSTRAINT FK_corps_classe_echelon_classe FOREIGN KEY (cce_cls_code) REFERENCES referentiel_fudpe_new.dbo.classe(cls_code),
	CONSTRAINT FK_corps_classe_echelon_corps FOREIGN KEY (cce_cps_code) REFERENCES referentiel_fudpe_new.dbo.corps(cps_code),
	CONSTRAINT FK_corps_classe_echelon_corps_classe_echelon FOREIGN KEY (cce_suivant) REFERENCES referentiel_fudpe_new.dbo.corps_classe_echelon(cce_id),
	CONSTRAINT FK_corps_classe_echelon_echelon FOREIGN KEY (cce_ech_code) REFERENCES referentiel_fudpe_new.dbo.echelon(ech_code)
);
 CREATE NONCLUSTERED INDEX cce_corps_classe_echelon ON referentiel_fudpe_new.dbo.corps_classe_echelon (  cce_cps_code ASC  , cce_cls_code ASC  , cce_ech_code ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;
 CREATE NONCLUSTERED INDEX cce_suivant ON referentiel_fudpe_new.dbo.corps_classe_echelon (  cce_suivant ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;


-- referentiel_fudpe_new.dbo.historique_piece_acte definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.historique_piece_acte;

CREATE TABLE referentiel_fudpe_new.dbo.historique_piece_acte (
	hpa_id int IDENTITY(1,1) NOT NULL,
	hpa_act_id int NOT NULL,
	hpa_code_piece_generee varchar(255) COLLATE French_CI_AS NOT NULL,
	hpa_date_generation date NULL,
	hpa_date_created datetime2 NULL,
	hpa_date_updated datetime2 NULL,
	hpa_num_etape_circuit int NULL,
	CONSTRAINT PK_historique_piece_acte PRIMARY KEY (hpa_id),
	CONSTRAINT FK_historique_piece_acte_acte FOREIGN KEY (hpa_act_id) REFERENCES referentiel_fudpe_new.dbo.acte(act_id)
);
 CREATE NONCLUSTERED INDEX hpa_act_id ON referentiel_fudpe_new.dbo.historique_piece_acte (  hpa_act_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;
 CREATE NONCLUSTERED INDEX hpa_code_piece_generee ON referentiel_fudpe_new.dbo.historique_piece_acte (  hpa_code_piece_generee ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;


-- referentiel_fudpe_new.dbo.parametrage_template_acte definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.parametrage_template_acte;

CREATE TABLE referentiel_fudpe_new.dbo.parametrage_template_acte (
	id int IDENTITY(1,1) NOT NULL,
	is_individuel bit NOT NULL,
	nature varchar(50) COLLATE French_CI_AS NOT NULL,
	type_corps varchar(15) COLLATE French_CI_AS NOT NULL,
	ref_model varchar(255) COLLATE French_CI_AS NOT NULL,
	sous_secteur varchar(7) COLLATE French_CI_AS NOT NULL,
	type_acte int NOT NULL,
	json_data varchar(1500) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK__parametr__3213E83F2BA94E41 PRIMARY KEY (id),
	CONSTRAINT FK_parametrage_template_acte_sous_secteur FOREIGN KEY (sous_secteur) REFERENCES referentiel_fudpe_new.dbo.sous_secteur(ssec_code),
	CONSTRAINT FK_parametrage_template_acte_type_acte FOREIGN KEY (type_acte) REFERENCES referentiel_fudpe_new.dbo.type_acte(tac_id)
);


-- referentiel_fudpe_new.dbo.parametrage_type_acte_workflow definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.parametrage_type_acte_workflow;

CREATE TABLE referentiel_fudpe_new.dbo.parametrage_type_acte_workflow (
	id int IDENTITY(1,1) NOT NULL,
	ref_engine varchar(15) COLLATE French_CI_AS NOT NULL,
	nature varchar(50) COLLATE French_CI_AS NOT NULL,
	type_acte int NOT NULL,
	sous_secteur varchar(7) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK__parametr__3213E83F4E635A44 PRIMARY KEY (id),
	CONSTRAINT FK_parametrage_type_acte_workflow_sous_secteur FOREIGN KEY (sous_secteur) REFERENCES referentiel_fudpe_new.dbo.sous_secteur(ssec_code),
	CONSTRAINT FK_parametrage_type_acte_workflow_type_acte FOREIGN KEY (type_acte) REFERENCES referentiel_fudpe_new.dbo.type_acte(tac_id)
);


-- referentiel_fudpe_new.dbo.reference_corps definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.reference_corps;

CREATE TABLE referentiel_fudpe_new.dbo.reference_corps (
	ref_cps_cps_code varchar(10) COLLATE French_CI_AS NOT NULL,
	ref_cps_ref_id int NOT NULL,
	CONSTRAINT PK__referenc__A22D54F6043B3007 PRIMARY KEY (ref_cps_cps_code,ref_cps_ref_id),
	CONSTRAINT FK_reference_corps_corps FOREIGN KEY (ref_cps_cps_code) REFERENCES referentiel_fudpe_new.dbo.corps(cps_code),
	CONSTRAINT FK_reference_corps_reference FOREIGN KEY (ref_cps_ref_id) REFERENCES referentiel_fudpe_new.dbo.reference(ref_id)
);


-- referentiel_fudpe_new.dbo.[structure] definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.[structure];

CREATE TABLE referentiel_fudpe_new.dbo.[structure] (
	str_code varchar(20) COLLATE French_CI_AS NOT NULL,
	str_libelle varchar(255) COLLATE French_CI_AS NOT NULL,
	str_description varchar(255) COLLATE French_CI_AS NULL,
	str_type_code varchar(10) COLLATE French_CI_AS NOT NULL,
	str_parent_code varchar(20) COLLATE French_CI_AS NULL,
	show bit NULL,
	CONSTRAINT PK__structur__03405BA7D2DE9EC4 PRIMARY KEY (str_code),
	CONSTRAINT FK_structure_structure FOREIGN KEY (str_parent_code) REFERENCES referentiel_fudpe_new.dbo.[structure](str_code),
	CONSTRAINT FK_structure_type_structure FOREIGN KEY (str_type_code) REFERENCES referentiel_fudpe_new.dbo.type_structure(typst_code)
);
 CREATE NONCLUSTERED INDEX str_parent_code ON referentiel_fudpe_new.dbo.structure (  str_parent_code ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;


-- referentiel_fudpe_new.dbo.type_absence definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.type_absence;

CREATE TABLE referentiel_fudpe_new.dbo.type_absence (
	typabs_id int IDENTITY(1,1) NOT NULL,
	typabs_motif varchar(255) COLLATE French_CI_AS NULL,
	typabs_duree int NULL,
	typabs_tac_id int NULL,
	CONSTRAINT PK_type_absence PRIMARY KEY (typabs_id),
	CONSTRAINT FK_type_absence_type_acte FOREIGN KEY (typabs_tac_id) REFERENCES referentiel_fudpe_new.dbo.type_acte(tac_id)
);


-- referentiel_fudpe_new.dbo.absence definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.absence;

CREATE TABLE referentiel_fudpe_new.dbo.absence (
	abs_id int NOT NULL,
	abs_date_debut date NULL,
	abs_date_fin date NULL,
	abs_typabs_id int NULL,
	CONSTRAINT PK_absence PRIMARY KEY (abs_id),
	CONSTRAINT FK_absence_type_absence FOREIGN KEY (abs_typabs_id) REFERENCES referentiel_fudpe_new.dbo.type_absence(typabs_id)
);


-- referentiel_fudpe_new.dbo.affectation definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.affectation;

CREATE TABLE referentiel_fudpe_new.dbo.affectation (
	aff_id int IDENTITY(1,1) NOT NULL,
	aff_str_code varchar(20) COLLATE French_CI_AS NOT NULL,
	aff_fct_code varchar(20) COLLATE French_CI_AS NOT NULL,
	aff_responsable bit NOT NULL,
	CONSTRAINT PK_affectation PRIMARY KEY (aff_id),
	CONSTRAINT FK_affectation_fonction FOREIGN KEY (aff_fct_code) REFERENCES referentiel_fudpe_new.dbo.fonction(fct_code),
	CONSTRAINT FK_affectation_structure FOREIGN KEY (aff_str_code) REFERENCES referentiel_fudpe_new.dbo.[structure](str_code)
);
 CREATE UNIQUE NONCLUSTERED INDEX UNIQUE_FONCTION_STRUCTURE ON referentiel_fudpe_new.dbo.affectation (  aff_str_code ASC  , aff_fct_code ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;


-- referentiel_fudpe_new.dbo.agent definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.agent;

CREATE TABLE referentiel_fudpe_new.dbo.agent (
	agt_id int IDENTITY(51101201,1) NOT NULL,
	agt_matricule_solde varchar(15) COLLATE French_CI_AS NULL,
	agt_cni varchar(25) COLLATE French_CI_AS NULL,
	agt_matricule_interne varchar(50) COLLATE French_CI_AS NULL,
	agt_prenom varchar(255) COLLATE French_CI_AS NULL,
	agt_nom varchar(255) COLLATE French_CI_AS NULL,
	agt_date_naissance date NULL,
	agt_lieu_naissance varchar(255) COLLATE French_CI_AS NULL,
	agt_adresse varchar(255) COLLATE French_CI_AS NULL,
	agt_genre varchar(5) COLLATE French_CI_AS NULL,
	agt_situation_matrimoniale varchar(50) COLLATE French_CI_AS NULL,
	agt_telephone varchar(15) COLLATE French_CI_AS NULL,
	agt_email varchar(255) COLLATE French_CI_AS NULL,
	agt_prenom_pere varchar(255) COLLATE French_CI_AS NULL,
	agt_prenom_mere varchar(255) COLLATE French_CI_AS NULL,
	agt_nom_mere varchar(255) COLLATE French_CI_AS NULL,
	agt_nb_enfants_charge int NULL,
	agt_date_derniere_situation date NULL,
	agt_date_derniere_position date NULL,
	agt_num_ordre varchar(255) COLLATE French_CI_AS NULL,
	agt_ref_syst_externe varchar(255) COLLATE French_CI_AS NULL,
	agt_ref_photo varchar(255) COLLATE French_CI_AS NULL,
	agt_cce_id int NULL,
	agt_pos_code varchar(3) COLLATE French_CI_AS NULL,
	agt_spe_code varchar(7) COLLATE French_CI_AS NULL,
	agt_affectation_id int NULL,
	agt_str_code varchar(20) COLLATE French_CI_AS NULL,
	agt_fct_code varchar(20) COLLATE French_CI_AS NULL,
	agt_user_id int NULL,
	agt_initiateur_id int NULL,
	agt_date_entree_service date NULL,
	agt_date_created datetime2 NULL,
	agt_date_updated datetime2 NULL,
	agt_ministere_code varchar(20) COLLATE French_CI_AS NULL,
	agt_deleted bit DEFAULT 0 NOT NULL,
	agt_date_deleted datetime2 NULL,
	agt_is_update_after_activation bit DEFAULT 0 NULL,
	agt_action varchar(100) COLLATE French_CI_AS NULL,
	agt_parent_id int NULL,
	CONSTRAINT PK__agent__205F9281B1881CBE PRIMARY KEY (agt_id),
	CONSTRAINT FK_agent_affectation FOREIGN KEY (agt_affectation_id) REFERENCES referentiel_fudpe_new.dbo.affectation(aff_id),
	CONSTRAINT FK_agent_corps_classe_echelon FOREIGN KEY (agt_cce_id) REFERENCES referentiel_fudpe_new.dbo.corps_classe_echelon(cce_id),
	CONSTRAINT FK_agent_ministere FOREIGN KEY (agt_ministere_code) REFERENCES referentiel_fudpe_new.dbo.[structure](str_code),
	CONSTRAINT FK_agent_position FOREIGN KEY (agt_pos_code) REFERENCES referentiel_fudpe_new.dbo.[position](pos_code),
	CONSTRAINT FK_agent_specialite FOREIGN KEY (agt_spe_code) REFERENCES referentiel_fudpe_new.dbo.specialite(spe_code)
);
 CREATE NONCLUSTERED INDEX UIX_AGENT_MATRICULE ON referentiel_fudpe_new.dbo.agent (  agt_matricule_solde ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX UIX_AGENT_USER_ID ON referentiel_fudpe_new.dbo.agent (  agt_user_id ASC  )  
	 WHERE  ([agt_user_id] IS NOT NULL)
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX agent_agt_user_id_IDX ON referentiel_fudpe_new.dbo.agent (  agt_user_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [AGENT ] ;
 CREATE NONCLUSTERED INDEX agent_recherche_multi_critere ON referentiel_fudpe_new.dbo.agent (  agt_nom ASC  , agt_matricule_solde ASC  , agt_cni ASC  , agt_prenom ASC  , agt_date_naissance ASC  , agt_cce_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [AGENT ] ;
 CREATE NONCLUSTERED INDEX agt_affectation_id ON referentiel_fudpe_new.dbo.agent (  agt_affectation_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [AGENT ] ;
 CREATE NONCLUSTERED INDEX agt_cce_id ON referentiel_fudpe_new.dbo.agent (  agt_cce_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [AGENT ] ;
 CREATE NONCLUSTERED INDEX agt_ministere_code ON referentiel_fudpe_new.dbo.agent (  agt_ministere_code ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [AGENT ] ;
 CREATE NONCLUSTERED INDEX agt_pos_code ON referentiel_fudpe_new.dbo.agent (  agt_pos_code ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [AGENT ] ;
 CREATE NONCLUSTERED INDEX agt_spe_code ON referentiel_fudpe_new.dbo.agent (  agt_spe_code ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [AGENT ] ;


-- referentiel_fudpe_new.dbo.agent_diplome definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.agent_diplome;

CREATE TABLE referentiel_fudpe_new.dbo.agent_diplome (
	dip_code varchar(10) COLLATE French_CI_AS NOT NULL,
	agent_id int NOT NULL,
	CONSTRAINT PK__agent_di__FC5C070266B4BB19 PRIMARY KEY (dip_code,agent_id),
	CONSTRAINT FK_agent_diplome_agent FOREIGN KEY (agent_id) REFERENCES referentiel_fudpe_new.dbo.agent(agt_id),
	CONSTRAINT FK_agent_diplome_diplome FOREIGN KEY (dip_code) REFERENCES referentiel_fudpe_new.dbo.diplome(dip_code)
);


-- referentiel_fudpe_new.dbo.anciennete definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.anciennete;

CREATE TABLE referentiel_fudpe_new.dbo.anciennete (
	anc_id int IDENTITY(1,1) NOT NULL,
	anc_valeur int NOT NULL,
	anc_date_anciennete date NOT NULL,
	anc_is_current bit NOT NULL,
	anc_agent_id int NOT NULL,
	CONSTRAINT PK__ancienne__3213E83F4AA0D14B PRIMARY KEY (anc_id),
	CONSTRAINT FK_anciennete_agent FOREIGN KEY (anc_agent_id) REFERENCES referentiel_fudpe_new.dbo.agent(agt_id)
);
 CREATE NONCLUSTERED INDEX anc_agent_id ON referentiel_fudpe_new.dbo.anciennete (  anc_agent_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;


-- referentiel_fudpe_new.dbo.commentaire_agent definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.commentaire_agent;

CREATE TABLE referentiel_fudpe_new.dbo.commentaire_agent (
	cmt_id int IDENTITY(1,1) NOT NULL,
	cmt_texte varchar(MAX) COLLATE French_CI_AS NULL,
	cmt_type_commentaire varchar(20) COLLATE French_CI_AS NOT NULL,
	cmt_agent_id int NOT NULL,
	cmt_date_created datetime2 NULL,
	cmt_date_updated datetime2 NULL,
	cmt_deleted bit DEFAULT 0 NOT NULL,
	cmt_date_deleted datetime2 NULL,
	cmt_act_id int NOT NULL,
	cmt_ref_GED varchar(255) COLLATE French_CI_AS NULL,
	cmt_eta_act_id int NOT NULL,
	cmt_type_motif_rejet varchar(255) COLLATE French_CI_AS NULL,
	CONSTRAINT PK__commenta__3213E83F8495873D PRIMARY KEY (cmt_id),
	CONSTRAINT FK_commentaire_agent_acte FOREIGN KEY (cmt_act_id) REFERENCES referentiel_fudpe_new.dbo.acte(act_id),
	CONSTRAINT FK_commentaire_agent_agent FOREIGN KEY (cmt_agent_id) REFERENCES referentiel_fudpe_new.dbo.agent(agt_id),
	CONSTRAINT FK_commentaire_agent_etat_acte FOREIGN KEY (cmt_eta_act_id) REFERENCES referentiel_fudpe_new.dbo.etat_acte(eta_act_id) ON DELETE CASCADE ON UPDATE CASCADE
);
 CREATE NONCLUSTERED INDEX cmt_act_id ON referentiel_fudpe_new.dbo.commentaire_agent (  cmt_act_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;
 CREATE NONCLUSTERED INDEX cmt_agent_id ON referentiel_fudpe_new.dbo.commentaire_agent (  cmt_agent_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;


-- referentiel_fudpe_new.dbo.corps_structure definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.corps_structure;

CREATE TABLE referentiel_fudpe_new.dbo.corps_structure (
	str_code varchar(20) COLLATE French_CI_AS NOT NULL,
	cps_code varchar(10) COLLATE French_CI_AS NOT NULL,
	CONSTRAINT PK__cadre_st__C8294B1A8A385FEF PRIMARY KEY (str_code,cps_code),
	CONSTRAINT FK_corps_structure_corps FOREIGN KEY (cps_code) REFERENCES referentiel_fudpe_new.dbo.corps(cps_code),
	CONSTRAINT FK_corps_structure_structure FOREIGN KEY (str_code) REFERENCES referentiel_fudpe_new.dbo.[structure](str_code)
);


-- referentiel_fudpe_new.dbo.dossier definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.dossier;

CREATE TABLE referentiel_fudpe_new.dbo.dossier (
	id int IDENTITY(1,1) NOT NULL,
	matricule_solde varchar(100) COLLATE French_CI_AS NULL,
	cni varchar(100) COLLATE French_CI_AS NULL,
	prenom varchar(100) COLLATE French_CI_AS NULL,
	nom varchar(100) COLLATE French_CI_AS NULL,
	situation_matrimoniale varchar(100) COLLATE French_CI_AS NULL,
	date_naissance date NULL,
	lieu_naissance varchar(100) COLLATE French_CI_AS NULL,
	adresse varchar(100) COLLATE French_CI_AS NULL,
	telephone varchar(100) COLLATE French_CI_AS NULL,
	email varchar(100) COLLATE French_CI_AS NULL,
	email_pro varchar(100) COLLATE French_CI_AS NULL,
	nb_enfants_charge varchar(100) COLLATE French_CI_AS NULL,
	ref_photo varchar(100) COLLATE French_CI_AS NULL,
	genre varchar(100) COLLATE French_CI_AS NULL,
	diplome_academie varchar(100) COLLATE French_CI_AS NULL,
	diplome_professionnel varchar(100) COLLATE French_CI_AS NULL,
	personne_contact varchar(100) COLLATE French_CI_AS NULL,
	telephone_contact varchar(100) COLLATE French_CI_AS NULL,
	date_entree_service date NULL,
	fonction varchar(100) COLLATE French_CI_AS NULL,
	dos_fichier varbinary(MAX) NULL,
	lien varchar(1000) COLLATE French_CI_AS NULL,
	dos_agt_id int NULL,
	dos_bordereau int NULL,
	dos_type_act int NULL,
	dos_etatdossier int NULL,
	DATE_CREATION datetime DEFAULT getdate() NULL,
	DATE_UPDATED datetime DEFAULT getdate() NULL,
	DELETED bit DEFAULT 0 NULL,
	DATE_DELETED datetime NULL,
	datebordereau date NULL,
	dos_agt_impute int NULL,
	dos_date_impute date NULL,
	motifrejet varchar(255) COLLATE French_CI_AS NULL,
	idprojet int NULL,
	dos_generated_file bit NULL,
	dos_nom_agent_traitant varchar(255) COLLATE French_CI_AS NULL,
	dos_structure varchar(20) COLLATE French_CI_AS NULL,
	CONSTRAINT PK__dossier__3213E83FC3152CB8 PRIMARY KEY (id),
	CONSTRAINT FK_dossier_agent FOREIGN KEY (dos_agt_id) REFERENCES referentiel_fudpe_new.dbo.agent(agt_id),
	CONSTRAINT FK_dossier_bordereau FOREIGN KEY (dos_bordereau) REFERENCES referentiel_fudpe_new.dbo.bordereau(id),
	CONSTRAINT FK_dossier_etatdossier FOREIGN KEY (dos_etatdossier) REFERENCES referentiel_fudpe_new.dbo.etat_dossier(id),
	CONSTRAINT FK_dossier_typeact FOREIGN KEY (dos_type_act) REFERENCES referentiel_fudpe_new.dbo.type_acte(tac_id),
	CONSTRAINT fk_dos_structure FOREIGN KEY (dos_structure) REFERENCES referentiel_fudpe_new.dbo.[structure](str_code)
);


-- referentiel_fudpe_new.dbo.historique_avancement definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.historique_avancement;

CREATE TABLE referentiel_fudpe_new.dbo.historique_avancement (
	hist_id int IDENTITY(1,1) NOT NULL,
	hist_act_id int DEFAULT NULL NULL,
	hist_agt_id int DEFAULT NULL NULL,
	hist_code_ech varchar(7) COLLATE French_CI_AS DEFAULT NULL NULL,
	hist_code_classe varchar(7) COLLATE French_CI_AS DEFAULT NULL NULL,
	hist_date_acte date DEFAULT NULL NULL,
	hist_date_effet date DEFAULT NULL NULL,
	hist_date_position date DEFAULT NULL NULL,
	hist_anc_conserv int DEFAULT NULL NULL,
	hist_lib_ech varchar(255) COLLATE French_CI_AS NULL,
	hist_lib_grade varchar(255) COLLATE French_CI_AS NULL,
	CONSTRAINT PK__historique_avancement PRIMARY KEY (hist_id),
	CONSTRAINT FK_historique_avancement_acte FOREIGN KEY (hist_act_id) REFERENCES referentiel_fudpe_new.dbo.acte(act_id),
	CONSTRAINT FK_historique_avancement_agent FOREIGN KEY (hist_agt_id) REFERENCES referentiel_fudpe_new.dbo.agent(agt_id)
);
 CREATE NONCLUSTERED INDEX hist_act_id ON referentiel_fudpe_new.dbo.historique_avancement (  hist_act_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;
 CREATE NONCLUSTERED INDEX hist_agt_id ON referentiel_fudpe_new.dbo.historique_avancement (  hist_agt_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;


-- referentiel_fudpe_new.dbo.historique_dossier definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.historique_dossier;

CREATE TABLE referentiel_fudpe_new.dbo.historique_dossier (
	id int IDENTITY(1,1) NOT NULL,
	matricule_solde varchar(100) COLLATE French_CI_AS NOT NULL,
	cni varchar(100) COLLATE French_CI_AS NOT NULL,
	prenom varchar(100) COLLATE French_CI_AS NOT NULL,
	nom varchar(100) COLLATE French_CI_AS NOT NULL,
	situation_matrimoniale varchar(100) COLLATE French_CI_AS NOT NULL,
	date_naissance date NOT NULL,
	lieu_naissance varchar(100) COLLATE French_CI_AS NOT NULL,
	adresse varchar(100) COLLATE French_CI_AS NOT NULL,
	telephone varchar(100) COLLATE French_CI_AS NOT NULL,
	email varchar(100) COLLATE French_CI_AS NOT NULL,
	email_pro varchar(100) COLLATE French_CI_AS NOT NULL,
	nb_enfants_charge varchar(100) COLLATE French_CI_AS NOT NULL,
	ref_photo varchar(100) COLLATE French_CI_AS NOT NULL,
	genre varchar(100) COLLATE French_CI_AS NOT NULL,
	diplome_academie varchar(100) COLLATE French_CI_AS NOT NULL,
	diplome_professionnel varchar(100) COLLATE French_CI_AS NOT NULL,
	personne_contact varchar(100) COLLATE French_CI_AS NOT NULL,
	telephone_contact varchar(100) COLLATE French_CI_AS NOT NULL,
	date_entree_service date NOT NULL,
	fonction varchar(100) COLLATE French_CI_AS NOT NULL,
	fichier varbinary(MAX) NOT NULL,
	lien varchar(100) COLLATE French_CI_AS NOT NULL,
	dos_agt_id int NOT NULL,
	dos_bordereau int NOT NULL,
	dos_type_act int NULL,
	dos_etatdossier int NOT NULL,
	DATE_CREATION datetime DEFAULT getdate() NULL,
	DATE_UPDATED datetime DEFAULT getdate() NULL,
	DELETED bit DEFAULT 0 NULL,
	DATE_DELETED datetime NULL,
	CONSTRAINT PK__historiq__3213E83F52EE82B9 PRIMARY KEY (id),
	CONSTRAINT FK_historique_dossier_agent FOREIGN KEY (dos_agt_id) REFERENCES referentiel_fudpe_new.dbo.agent(agt_id),
	CONSTRAINT FK_historique_dossier_bordereau FOREIGN KEY (dos_bordereau) REFERENCES referentiel_fudpe_new.dbo.bordereau(id),
	CONSTRAINT FK_historique_dossier_etatdossier FOREIGN KEY (dos_etatdossier) REFERENCES referentiel_fudpe_new.dbo.etat_dossier(id),
	CONSTRAINT FK_historique_dossier_typeacte FOREIGN KEY (dos_type_act) REFERENCES referentiel_fudpe_new.dbo.type_acte(tac_id)
);


-- referentiel_fudpe_new.dbo.historique_men definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.historique_men;

CREATE TABLE referentiel_fudpe_new.dbo.historique_men (
	id int IDENTITY(1,1) NOT NULL,
	his_men_commentaire nvarchar(MAX) COLLATE French_CI_AS NULL,
	his_men_operation nvarchar(255) COLLATE French_CI_AS NOT NULL,
	his_men_reponse nvarchar(MAX) COLLATE French_CI_AS NULL,
	hist_men_agt_id int NOT NULL,
	hist_men_dos_id int NOT NULL,
	CONSTRAINT PK__historiq__3213E83FDA71625D PRIMARY KEY (id),
	CONSTRAINT FK_HistoriqueMen_Agent FOREIGN KEY (hist_men_agt_id) REFERENCES referentiel_fudpe_new.dbo.agent(agt_id),
	CONSTRAINT FK_HistoriqueMen_Dossier FOREIGN KEY (hist_men_dos_id) REFERENCES referentiel_fudpe_new.dbo.dossier(id)
);


-- referentiel_fudpe_new.dbo.historique_projet_acte definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.historique_projet_acte;

CREATE TABLE referentiel_fudpe_new.dbo.historique_projet_acte (
	hist_id int IDENTITY(1,1) NOT NULL,
	hist_act_id int NOT NULL,
	hist_agent_id int NOT NULL,
	hist_etat_projet_id int NOT NULL,
	hist_date_created datetime2 NOT NULL,
	hist_date_updated datetime2 NULL,
	CONSTRAINT PK_historique_projet_acte PRIMARY KEY (hist_id),
	CONSTRAINT FK_historique_projet_acte_acte FOREIGN KEY (hist_act_id) REFERENCES referentiel_fudpe_new.dbo.acte(act_id),
	CONSTRAINT FK_historique_projet_acte_agent FOREIGN KEY (hist_agent_id) REFERENCES referentiel_fudpe_new.dbo.agent(agt_id),
	CONSTRAINT FK_historique_projet_acte_etat_projet FOREIGN KEY (hist_etat_projet_id) REFERENCES referentiel_fudpe_new.dbo.etat_projet(etp_id)
);
 CREATE NONCLUSTERED INDEX hist_act_id ON referentiel_fudpe_new.dbo.historique_projet_acte (  hist_act_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;
 CREATE NONCLUSTERED INDEX hist_agent_id ON referentiel_fudpe_new.dbo.historique_projet_acte (  hist_agent_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;


-- referentiel_fudpe_new.dbo.imputation definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.imputation;

CREATE TABLE referentiel_fudpe_new.dbo.imputation (
	imp_id int IDENTITY(1,1) NOT NULL,
	imp_date_created datetime NULL,
	imp_date_updated datetime NULL,
	imp_avis varchar(10) COLLATE French_CI_AS NULL,
	imp_commentaire_imputeur varchar(500) COLLATE French_CI_AS NULL,
	imp_commentaire_impute varchar(MAX) COLLATE French_CI_AS NULL,
	imp_date_avis datetime NULL,
	imp_acte_id int NOT NULL,
	imp_agent_impute_id int NOT NULL,
	imp_agent_imputeur_id int NOT NULL,
	imp_ref_GED varchar(255) COLLATE French_CI_AS NULL,
	imp_traite bit DEFAULT 0 NOT NULL,
	CONSTRAINT PK_imputation PRIMARY KEY (imp_id),
	CONSTRAINT FK_imputation_acte FOREIGN KEY (imp_acte_id) REFERENCES referentiel_fudpe_new.dbo.acte(act_id),
	CONSTRAINT FK_imputation_agent_impute FOREIGN KEY (imp_agent_impute_id) REFERENCES referentiel_fudpe_new.dbo.agent(agt_id),
	CONSTRAINT FK_imputation_agent_imputeur FOREIGN KEY (imp_agent_imputeur_id) REFERENCES referentiel_fudpe_new.dbo.agent(agt_id)
);
 CREATE NONCLUSTERED INDEX imp_acte_id ON referentiel_fudpe_new.dbo.imputation (  imp_acte_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;
 CREATE NONCLUSTERED INDEX imp_agent_impute_id ON referentiel_fudpe_new.dbo.imputation (  imp_agent_impute_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;
 CREATE NONCLUSTERED INDEX imp_agent_imputeur_id ON referentiel_fudpe_new.dbo.imputation (  imp_agent_imputeur_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;


-- referentiel_fudpe_new.dbo.message definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.message;

CREATE TABLE referentiel_fudpe_new.dbo.message (
	msg_id int IDENTITY(1,1) NOT NULL,
	msg_agent_id int NOT NULL,
	msg_objet varchar(100) COLLATE French_CI_AS NOT NULL,
	msg_texte varchar(MAX) COLLATE French_CI_AS NOT NULL,
	msg_date_created datetime2 NOT NULL,
	msg_date_updated datetime2 NULL,
	msg_lu bit NOT NULL,
	msg_deleted bit DEFAULT 0 NOT NULL,
	msg_date_deleted datetime2 NULL,
	CONSTRAINT PK_message PRIMARY KEY (msg_id),
	CONSTRAINT FK_message_agent FOREIGN KEY (msg_agent_id) REFERENCES referentiel_fudpe_new.dbo.agent(agt_id)
);
 CREATE NONCLUSTERED INDEX msg_agent_id ON referentiel_fudpe_new.dbo.message (  msg_agent_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [SECONDARY ] ;


-- referentiel_fudpe_new.dbo.reclamation definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.reclamation;

CREATE TABLE referentiel_fudpe_new.dbo.reclamation (
	recl_agt_id int NOT NULL,
	recl_type nvarchar(50) COLLATE French_CI_AS NULL,
	recl_texte nvarchar(500) COLLATE French_CI_AS NOT NULL,
	recl_file_name nvarchar(250) COLLATE French_CI_AS NOT NULL,
	recl_file_type nvarchar(255) COLLATE French_CI_AS NOT NULL,
	recl_file_size bigint NOT NULL,
	recl_file_data varbinary(MAX) NOT NULL,
	recl_is_treated bit NOT NULL,
	recl_agent_treated int NULL,
	recl_is_deleted bit NOT NULL,
	recl_date_created datetime2(0) NULL,
	recl_date_updated datetime2(0) NULL,
	recl_date_deleted datetime2(0) NULL,
	recl_deleted bit NULL,
	recl_id bigint IDENTITY(1,1) NOT NULL,
	recl_libelle_type varchar(50) COLLATE French_CI_AS NULL,
	recl_type_rejet varchar(50) COLLATE French_CI_AS NULL,
	recl_libelle_type_rejet varchar(50) COLLATE French_CI_AS NULL,
	recl_motif_rejet varchar(500) COLLATE French_CI_AS NULL,
	CONSTRAINT PK_Reclamation PRIMARY KEY (recl_id),
	CONSTRAINT FK_Reclamation_Agent FOREIGN KEY (recl_agt_id) REFERENCES referentiel_fudpe_new.dbo.agent(agt_id)
);


-- referentiel_fudpe_new.dbo.acte_agent definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.acte_agent;

CREATE TABLE referentiel_fudpe_new.dbo.acte_agent (
	act_agt_id int IDENTITY(1,1) NOT NULL,
	act_agt_act_id int NOT NULL,
	act_agt_agt_id int NOT NULL,
	act_agt_cce_id int NULL,
	act_agt_fct_code varchar(20) COLLATE French_CI_AS NULL,
	act_agt_str_code varchar(20) COLLATE French_CI_AS NULL,
	act_agt_spe_code varchar(7) COLLATE French_CI_AS NULL,
	act_agt_pos_code varchar(3) COLLATE French_CI_AS NULL,
	act_agt_date_effet date NOT NULL,
	act_agt_date_created datetime2 NULL,
	act_agt_date_updated datetime2 NULL,
	act_agt_deleted bit DEFAULT 0 NOT NULL,
	act_agt_date_deleted datetime2 NULL,
	act_agt_dip_code varchar(10) COLLATE French_CI_AS NULL,
	act_agt_session_diplome char(4) COLLATE French_CI_AS NULL,
	act_agt_date_obtention_diplome date NULL,
	act_poste_budgetaire_libere varchar(255) COLLATE French_CI_AS NULL,
	act_agt_date_entree_service date NULL,
	act_observations varchar(255) COLLATE French_CI_AS NULL,
	act_agt_pays_code varchar(20) COLLATE French_CI_AS DEFAULT NULL NULL,
	act_agt_pays_id int DEFAULT NULL NULL,
	act_agt_date_avis_mutation date DEFAULT NULL NULL,
	act_agt_note_globale varchar(255) COLLATE French_CI_AS DEFAULT NULL NULL,
	act_agt_taux_mensuel decimal(10,0) DEFAULT NULL NULL,
	act_agt_agt_remplace_id int DEFAULT NULL NULL,
	act_agt_motif_remplacement varchar(250) COLLATE French_CI_AS DEFAULT NULL NULL,
	act_poste_budgetaire_accueil varchar(255) COLLATE French_CI_AS NULL,
	act_agt_date_debut date NULL,
	act_agt_date_fin date NULL,
	act_agt_duree int NULL,
	act_agt_date_deces date NULL,
	act_agt_lieu_deces varchar(255) COLLATE French_CI_AS NULL,
	act_agt_des_id int NULL,
	act_agt_etablissement varchar(256) COLLATE French_CI_AS NULL,
	act_agt_duree_indemnite int NULL,
	act_agt_montant int NULL,
	act_agt_duree_stage int NULL,
	CONSTRAINT PK__acte_age__F94478B7D2CAAC4D PRIMARY KEY (act_agt_id),
	CONSTRAINT FK_acte_agent_acte FOREIGN KEY (act_agt_act_id) REFERENCES referentiel_fudpe_new.dbo.acte(act_id),
	CONSTRAINT FK_acte_agent_agent FOREIGN KEY (act_agt_agt_id) REFERENCES referentiel_fudpe_new.dbo.agent(agt_id),
	CONSTRAINT FK_acte_agent_corps_classe_echelon FOREIGN KEY (act_agt_cce_id) REFERENCES referentiel_fudpe_new.dbo.corps_classe_echelon(cce_id),
	CONSTRAINT FK_acte_agent_diplome FOREIGN KEY (act_agt_dip_code) REFERENCES referentiel_fudpe_new.dbo.diplome(dip_code),
	CONSTRAINT FK_acte_agent_fonction FOREIGN KEY (act_agt_fct_code) REFERENCES referentiel_fudpe_new.dbo.fonction(fct_code),
	CONSTRAINT FK_acte_agent_position FOREIGN KEY (act_agt_pos_code) REFERENCES referentiel_fudpe_new.dbo.[position](pos_code),
	CONSTRAINT FK_acte_agent_specialite FOREIGN KEY (act_agt_spe_code) REFERENCES referentiel_fudpe_new.dbo.specialite(spe_code),
	CONSTRAINT FK_acte_agent_structure FOREIGN KEY (act_agt_str_code) REFERENCES referentiel_fudpe_new.dbo.[structure](str_code)
);
 CREATE NONCLUSTERED INDEX act_agt_act_id ON referentiel_fudpe_new.dbo.acte_agent (  act_agt_act_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [AGENT_ACTE ] ;
 CREATE NONCLUSTERED INDEX act_agt_agt_id ON referentiel_fudpe_new.dbo.acte_agent (  act_agt_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [AGENT_ACTE ] ;
 CREATE NONCLUSTERED INDEX act_agt_cce_id ON referentiel_fudpe_new.dbo.acte_agent (  act_agt_cce_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [AGENT_ACTE ] ;


-- referentiel_fudpe_new.dbo.anciennetes definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.anciennetes;

CREATE TABLE referentiel_fudpe_new.dbo.anciennetes (
	ancs_id int NOT NULL,
	ancs_date_debut date NULL,
	ancs_date_fin date NULL,
	ancs_anciennete int NULL,
	ancs_code_corps varchar(10) COLLATE French_CI_AS NULL,
	ancs_code_classe varchar(7) COLLATE French_CI_AS NULL,
	ancs_code_echelon varchar(7) COLLATE French_CI_AS NULL,
	ancs_date_debut_disponibilite date NULL,
	ancs_date_fin_disponibilite date NULL,
	CONSTRAINT PK_anciennetes PRIMARY KEY (ancs_id),
	CONSTRAINT FK_anciennetes_acte_agent FOREIGN KEY (ancs_id) REFERENCES referentiel_fudpe_new.dbo.acte_agent(act_agt_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT FK_anciennetes_classe FOREIGN KEY (ancs_code_classe) REFERENCES referentiel_fudpe_new.dbo.classe(cls_code),
	CONSTRAINT FK_anciennetes_corps FOREIGN KEY (ancs_code_corps) REFERENCES referentiel_fudpe_new.dbo.corps(cps_code),
	CONSTRAINT FK_anciennetes_echelon FOREIGN KEY (ancs_code_echelon) REFERENCES referentiel_fudpe_new.dbo.echelon(ech_code)
);


-- referentiel_fudpe_new.dbo.conge definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.conge;

CREATE TABLE referentiel_fudpe_new.dbo.conge (
	cng_id int NOT NULL,
	cng_date_debut date NOT NULL,
	cng_date_fin date NOT NULL,
	CONSTRAINT PK_conge PRIMARY KEY (cng_id),
	CONSTRAINT FK_conge_acte_agent FOREIGN KEY (cng_id) REFERENCES referentiel_fudpe_new.dbo.acte_agent(act_agt_id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- referentiel_fudpe_new.dbo.sortie_temporaire definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.sortie_temporaire;

CREATE TABLE referentiel_fudpe_new.dbo.sortie_temporaire (
	st_id int NOT NULL,
	st_dateDebut date NOT NULL,
	st_dateFin date NULL,
	st_duree int NULL,
	st_renouvellement int NULL,
	st_observations varchar(255) COLLATE French_CI_AS NULL,
	st_poste_budgetaire_accueil varchar(255) COLLATE French_CI_AS NULL,
	st_type_sortie_id int NOT NULL,
	CONSTRAINT PK__sortiete__A85E81CFED2F28DB PRIMARY KEY (st_id),
	CONSTRAINT FK_sortie_temporaire_acte_agent FOREIGN KEY (st_id) REFERENCES referentiel_fudpe_new.dbo.acte_agent(act_agt_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT FK_sortie_temporaire_type_sortie_temporaire FOREIGN KEY (st_type_sortie_id) REFERENCES referentiel_fudpe_new.dbo.type_sortie_temporaire(tst_id)
);


-- referentiel_fudpe_new.dbo.validation_anciennete definition

-- Drop table

-- DROP TABLE referentiel_fudpe_new.dbo.validation_anciennete;

CREATE TABLE referentiel_fudpe_new.dbo.validation_anciennete (
	id int NOT NULL,
	date_debut_volontariat date NULL,
	date_fin_volontariat date NULL,
	date_debut_contractuel date NULL,
	date_fin_contractuel date NULL,
	date_debut_sortie_temporaire date NULL,
	date_fin_sortie_temporaire date NULL,
	pourcentage_prise_en_compte decimal(5,0) NULL,
	duree_sortie_temporaire int NULL,
	anciennete_totale int NOT NULL,
	anciennete_conservee int NOT NULL,
	CONSTRAINT PK__validati__3213E83FCBBAA535 PRIMARY KEY (id),
	CONSTRAINT FK_validation_anciennete_acte_agent FOREIGN KEY (id) REFERENCES referentiel_fudpe_new.dbo.acte_agent(act_agt_id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- dbo.ActesDisponiblesParType source

ALTER VIEW ActesDisponiblesParType  AS
SELECT 
    a.act_id,
    a.act_numero_projet,
    ta.tac_libelle AS Type_acte,
    a.act_date_acte,
    COUNT(aa.act_agt_id) AS nombre_agent
FROM referentiel_fudpe_new.dbo.acte a
JOIN referentiel_fudpe_new.dbo.type_acte ta 
    ON a.act_tac_id = ta.tac_id
LEFT JOIN referentiel_fudpe_new.dbo.acte_agent aa 
    ON a.act_id = aa.act_agt_act_id  
    AND aa.act_agt_deleted = 0
WHERE a.act_is_projet = 0
  AND a.act_deleted = 0
  AND a.act_etat_id IN (24)
  AND a.act_process_instance_id IS NOT NULL
GROUP BY a.act_id, a.act_numero_projet, ta.tac_libelle, a.act_date_acte;


-- dbo.ProjetsActesParType source

ALTER VIEW ProjetsActesParType AS
SELECT 
    a.act_id,
    a.act_numero_projet,
    ta.tac_libelle AS Type_acte,
    a.act_date_projet
FROM referentiel_fudpe_new.dbo.acte a
JOIN referentiel_fudpe_new.dbo.type_acte ta 
    ON a.act_tac_id = ta.tac_id
WHERE a.act_is_projet = 1
  AND a.act_deleted = 0
  AND a.act_etat_id NOT IN (24)
  AND a.act_process_instance_id IS NOT NULL;


-- dbo.Projets_Etats_V source

ALTER VIEW dbo.v_projets_etats AS
SELECT 
    (SELECT COUNT(*) 
     FROM referentiel_fudpe_new.dbo.acte a 
     WHERE a.act_is_projet = 1
       AND a.act_deleted = 0
       AND a.act_date_projet >= '2023-08-10'
       AND a.act_etat_id IN (13, 35, 533)
       AND a.act_process_instance_id IS NOT NULL) AS ministre,

    (SELECT COUNT(*) 
     FROM referentiel_fudpe_new.dbo.acte a 
     WHERE a.act_is_projet = 1
       AND a.act_deleted = 0
       AND a.act_date_projet >= '2023-08-10'
       AND a.act_etat_id IN (12, 38, 532)
       AND a.act_process_instance_id IS NOT NULL) AS numeroteur,

    (SELECT COUNT(*) 
     FROM referentiel_fudpe_new.dbo.acte a 
     WHERE a.act_is_projet = 1
       AND a.act_deleted = 0
       AND a.act_date_projet >= '2023-08-10'
       AND a.act_etat_id IN (11, 36, 494, 510, 447, 549)
       AND a.act_process_instance_id IS NOT NULL) AS sgg,

    (SELECT COUNT(*) 
     FROM referentiel_fudpe_new.dbo.acte a 
     WHERE a.act_is_projet = 1
       AND a.act_deleted = 0
       AND a.act_date_projet >= '2023-08-10'
       AND a.act_etat_id IN (23, 34, 503, 504, 560)
       AND a.act_process_instance_id IS NOT NULL) AS sg_dc,

    (SELECT COUNT(*) 
     FROM referentiel_fudpe_new.dbo.acte a 
     WHERE a.act_is_projet = 1
       AND a.act_deleted = 0
       AND a.act_date_projet >= '2023-08-10'
       AND a.act_etat_id IN (10, 33, 497, 501)
       AND a.act_process_instance_id IS NOT NULL) AS dgfp,

    (SELECT COUNT(*) 
     FROM referentiel_fudpe_new.dbo.acte a 
     WHERE a.act_is_projet = 1
       AND a.act_deleted = 0
       AND a.act_date_projet >= '2023-08-10'
       AND a.act_etat_id IN (6, 500, 524, 543)
       AND a.act_process_instance_id IS NOT NULL) AS controle_financier,

    (SELECT COUNT(*) 
     FROM referentiel_fudpe_new.dbo.acte a 
     WHERE a.act_is_projet = 1
       AND a.act_deleted = 0
       AND a.act_date_projet >= '2023-08-10'
       AND a.act_etat_id IN (9, 499, 529, 544)
       AND a.act_process_instance_id IS NOT NULL) AS dpb,

    (SELECT COUNT(*) 
     FROM referentiel_fudpe_new.dbo.acte a 
     WHERE a.act_is_projet = 1
       AND a.act_deleted = 0
       AND a.act_date_projet >= '2023-08-10'
       AND a.act_etat_id IN (551, 553)
       AND a.act_process_instance_id IS NOT NULL) AS dp,

    (SELECT COUNT(*) 
     FROM referentiel_fudpe_new.dbo.acte a 
     WHERE a.act_is_projet = 1
       AND a.act_deleted = 0
       AND a.act_date_projet >= '2023-08-10'
       AND a.act_etat_id IN (7, 498, 523, 542)
       AND a.act_process_instance_id IS NOT NULL) AS dcems,

    (SELECT COUNT(*) 
     FROM referentiel_fudpe_new.dbo.acte a 
     WHERE a.act_is_projet = 1
       AND a.act_deleted = 0
       AND a.act_date_projet >= '2023-08-10'
       AND a.act_etat_id IN (8, 37, 39, 488, 495, 531, 546)
       AND a.act_process_instance_id IS NOT NULL) AS svisa;


-- dbo.Projets_Rejetes_Par_Agent_v source

ALTER VIEW vue_projets_rejetes_par_agent AS
SELECT 
    CONCAT(a2.agt_nom, ' ', a2.agt_prenom, ' (', a2.agt_matricule_solde , ')') AS agent_info,
    CASE 
        WHEN a.act_str_initiateur = 'ST20005' THEN 'B1'
        WHEN a.act_str_initiateur = 'ST20006' THEN 'B10'
        WHEN a.act_str_initiateur = 'ST20007' THEN 'B12'
        WHEN a.act_str_initiateur = 'ST20008' THEN 'B13'
        WHEN a.act_str_initiateur = 'ST20009' THEN 'B2'
        WHEN a.act_str_initiateur = 'ST20010' THEN 'B8'
        WHEN a.act_str_initiateur = 'ST20011' THEN 'B9'
        WHEN a.act_str_initiateur = 'ST20015' THEN 'B14'
        WHEN a.act_str_initiateur = 'ST20016' THEN 'B4'
        WHEN a.act_str_initiateur = 'ST20017' THEN 'B3'
        WHEN a.act_str_initiateur = 'ST20018' THEN 'B11'
        WHEN a.act_str_initiateur = 'ST20020' THEN 'B6'
        WHEN a.act_str_initiateur = 'ST20021' THEN 'B7'
        WHEN a.act_str_initiateur = 'ST50005' THEN 'B5'
        WHEN a.act_str_initiateur = 'ST55555' THEN 'B50'
        WHEN a.act_str_initiateur = 'ST20001' THEN 'DENS'
        WHEN a.act_str_initiateur = 'ST20002' THEN 'DF'
        WHEN a.act_str_initiateur = 'ST20003' THEN 'DNF'
        WHEN a.act_str_initiateur = 'ST60006' THEN 'DPR'
        ELSE 'Autre'
    END AS bureau,
    COUNT(*) AS nombre_projets_rejetes
FROM 
    referentiel_fudpe_new.dbo.acte a
    JOIN referentiel_fudpe_new.dbo.agent a2 ON a.act_initiateur_id = a2.agt_id
WHERE 
    a.act_is_projet = 1
    AND a.act_deleted = 0
    AND a.act_etat_id IN (2, 493, 550)  -- états des projets rejetés
    AND a.act_date_projet >= '10/08/2024'
    AND a.act_process_instance_id IS NOT NULL
GROUP BY 
    a2.agt_nom, a2.agt_prenom, a2.agt_matricule_solde , a.act_str_initiateur;


-- dbo.v_agent_details source

-- dbo.Agent_Details_V source

ALTER VIEW dbo.v_agent_details AS
SELECT 
    a.agt_matricule_solde, 
    a.agt_cni, 
    a.agt_prenom, 
    a.agt_nom, 
    a.agt_date_naissance, 
    a.agt_lieu_naissance, 
    a.agt_situation_matrimoniale, 
    a.agt_genre, 
    c.cps_libelle, 
    c2.cad_libelle, 
    h.hier_libelle, 
    c.cps_typecorps_code 
FROM dbo.agent a
JOIN dbo.corps_classe_echelon cce 
    ON a.agt_cce_id = cce.cce_id
JOIN dbo.corps c 
    ON cce.cce_cps_code = c.cps_code
JOIN dbo.cadre c2 
    ON c.cps_cadre_code = c2.cad_code
JOIN dbo.hierarchie h 
    ON c.cps_hierarchie_code = h.hier_code
WHERE a.agt_deleted = 0;


-- dbo.vue_projets_rejetes_par_agent_et_type source

ALTER VIEW vue_projets_rejetes_par_agent_et_type AS
SELECT 
    CONCAT(a2.agt_nom, ' ', a2.agt_prenom, ' (', a2.agt_matricule_solde , ')') AS agent_info,
    CASE 
        WHEN a.act_str_initiateur = 'ST20005' THEN 'B1'
        WHEN a.act_str_initiateur = 'ST20006' THEN 'B10'
        WHEN a.act_str_initiateur = 'ST20007' THEN 'B12'
        WHEN a.act_str_initiateur = 'ST20008' THEN 'B13'
        WHEN a.act_str_initiateur = 'ST20009' THEN 'B2'
        WHEN a.act_str_initiateur = 'ST20010' THEN 'B8'
        WHEN a.act_str_initiateur = 'ST20011' THEN 'B9'
        WHEN a.act_str_initiateur = 'ST20015' THEN 'B14'
        WHEN a.act_str_initiateur = 'ST20016' THEN 'B4'
        WHEN a.act_str_initiateur = 'ST20017' THEN 'B3'
        WHEN a.act_str_initiateur = 'ST20018' THEN 'B11'
        WHEN a.act_str_initiateur = 'ST20020' THEN 'B6'
        WHEN a.act_str_initiateur = 'ST20021' THEN 'B7'
        WHEN a.act_str_initiateur = 'ST50005' THEN 'B5'
        WHEN a.act_str_initiateur = 'ST55555' THEN 'B50'
        WHEN a.act_str_initiateur = 'ST20001' THEN 'DENS'
        WHEN a.act_str_initiateur = 'ST20002' THEN 'DF'
        WHEN a.act_str_initiateur = 'ST20003' THEN 'DNF'
        WHEN a.act_str_initiateur = 'ST60006' THEN 'DPR'
        ELSE 'Autre'
    END AS bureau,
    ta.tac_libelle AS type_acte,
    COUNT(*) AS nombre_projets_rejetes
FROM 
    referentiel_fudpe_new.dbo.acte a
    JOIN referentiel_fudpe_new.dbo.agent a2 ON a.act_initiateur_id = a2.agt_id
    JOIN referentiel_fudpe_new.dbo.type_acte ta ON a.act_tac_id = ta.tac_id
WHERE 
    a.act_is_projet = 1
    AND a.act_deleted = 0
    AND a.act_etat_id IN (2, 493, 550)  -- états des projets rejetés
    AND a.act_date_projet >= '10/08/2024'
    AND a.act_process_instance_id IS NOT NULL
GROUP BY 
    a2.agt_nom, a2.agt_prenom, a2.agt_matricule_solde , a.act_str_initiateur, ta.tac_libelle;