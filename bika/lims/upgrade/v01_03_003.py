# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE.
#
# SENAITE.CORE is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2019 by it's authors.
# Some rights reserved, see README and LICENSE.

from Products.Archetypes.config import UID_CATALOG

from bika.lims import api
from bika.lims import logger
from bika.lims.catalog.bikasetup_catalog import SETUP_CATALOG
from bika.lims.config import PROJECTNAME as product
from bika.lims.setuphandlers import setup_form_controller_actions
from bika.lims.upgrade import upgradestep
from bika.lims.upgrade.utils import UpgradeUtils

version = "1.3.3"  # Remember version number in metadata.xml and setup.py
profile = "profile-{0}:default".format(product)

INDEXES_TO_ADD = [
    # Replaces getSampleTypeUIDs
    ("bika_setup_catalog", "sampletype_uid", "KeywordIndex"),

    # Replaces getSampleTypeTitle
    ("bika_setup_catalog", "sampletype_title", "KeywordIndex"),

    # Replaces getAvailableMethodUIDs
    # Used to filter services in Worksheet's Add Analyses View for when the
    # Worksheet Template being used has a Method assigned
    ("bika_setup_catalog", "method_available_uid", "KeywordIndex"),

    # Replaces getInstrumentTitle
    # Used for sorting Worksheet Templates listing by Instrument
    ("bika_setup_catalog", "instrument_title", "KeywordIndex"),

    # Replaces getPrice, getTotalPrice, getVolume
    # Used for sorting LabProducts listing
    ("bika_setup_catalog", "price", "FieldIndex"),
    ("bika_setup_catalog", "price_total", "FieldIndex"),

    # Replaces getInstrumentTypeName
    ("bika_setup_catalog", "instrumenttype_title", "KeywordIndex"),

    # Replaces getDepartmentTitle
    ("bika_setup_catalog", "department_title", "KeywordIndex"),

    # Replaces getPointOfCapture
    ("bika_setup_catalog", "point_of_capture", "FieldIndex"),

    # Replaces getDepartmentUID
    ("bika_setup_catalog", "department_uid", "KeywordIndex"),

    # Default listing_searchable_text index adapter for setup_catalog
    ("bika_setup_catalog", "listing_searchable_text", "TextIndexNG3"),

    # Default listing_searchable_text index adapter for setup_catalog
    ("bika_setup_catalog", "category_uid", "KeywordIndex"),
]

INDEXES_TO_REMOVE = [
    # Only used in add2 to filter Sample Points by Sample Type when a Sample
    # Type was selected. Now, getSampleTypeUID is used instead because of
    ("bika_setup_catalog", "getSampleTypeTitles"),

    # Only used for when Sample and SamplePartition objects
    # existed. The following are the portal types stored in bika_catalog:
    #   Batch, BatchFolder and ReferenceSample
    # and there are no searches by getSampleTypeTitle for none of them
    ("bika_catalog", "getSampleTypeTitle"),

    # Not used neither for searches nor filtering of any of the content types
    # stored in bika_catalog (Batch, BatchFolder and ReferenceSample)
    ("bika_catalog", "getSampleTypeUID"),

    # getAccredited was only used in the "hidden" view accreditation to filter
    # services labeled as "accredited". Since we don't expect that listing to
    # contain too many items, they are now filtered by waking-up the object
    ("bika_setup_catalog", "getAccredited"),

    # getAnalyst index is used in Analyses (Duplicates and Reference included)
    # and Worksheets. None of the types stored in setup_catalog support Analyst
    ("bika_setup_catalog", "getAnalyst"),

    # getBlank index is not used in setup_catalog, but in bika_catalog, where
    # is used in AddControl and AddBlank views (Worksheet)
    ("bika_setup_catalog", "getBlank"),

    # Only used in analyses listing, but from analysis_catalog
    ("bika_setup_catalog", "getCalculationUID"),

    # Only used for sorting in LabContacts listing. Replaced by sortable_title
    ("bika_setup_catalog", "getFullname"),

    # Used in analysis_catalog, but not in setup_catalog
    ("bika_setup_catalog", "getServiceUID"),

    # Not used anywhere
    ("bika_setup_catalog", "getDocumentID"),
    ("bika_setup_catalog", "getDuplicateVariation"),
    ("bika_setup_catalog", "getFormula"),
    ("bika_setup_catalog", "getInstrumentLocationName"),
    ("bika_setup_catalog", "getInstrumentType"),
    ("bika_setup_catalog", "getHazardous"),
    ("bika_setup_catalog", "getManagerEmail"),
    ("bika_setup_catalog", "getManagerPhone"),
    ("bika_setup_catalog", "getManagerName"),
    ("bika_setup_catalog", "getMethodID"),
    ("bika_setup_catalog", "getMaxTimeAllowed"),
    ("bika_setup_catalog", "getModel"),
    ("bika_setup_catalog", "getCalculationTitle"),
    ("bika_setup_catalog", "getCalibrationExpiryDate"),
    ("bika_setup_catalog", "getVATAmount"),
    ("bika_setup_catalog", "getUnit"),
    ("bika_setup_catalog", "getSamplePointTitle"),
    ("bika_setup_catalog", "getVolume"),
    ("bika_setup_catalog", "getSamplePointUID"),
    ("bika_setup_catalog", "getCategoryTitle"),
    ("bika_setup_catalog", "cancellation_state"),
    ("bika_setup_catalog", "getName"),
    ("bika_setup_catalog", "getServiceUIDs"),
    ("bika_setup_catalog", "SearchableText"),


    # REPLACEMENTS (indexes to be removed because of a replacement)

    # getSampleTypeUID --> sampletype_uid (FieldIndex --> KeywordIndex)
    ("bika_setup_catalog", "getSampleTypeUID"),
    ("bika_setup_catalog", "sampletype_uids"),

    # getSampleTypeTitle --> sampletype_title
    ("bika_setup_catalog", "getSampleTypeTitle"),

    # getAvailableMethodUIDs --> method_available_uid
    ("bika_setup_catalog", "getAvailableMethodUIDs"),

    # getInstrumentTitle --> instrument_title
    ("bika_setup_catalog", "getInstrumentTitle"),

    # getPrice --> price
    ("bika_setup_catalog", "getPrice"),

    # getTotalPrice --> price_total
    ("bika_setup_catalog", "getTotalPrice"),

    # getInstrumentTypeName --> instrumenttype_title
    ("bika_setup_catalog", "getInstrumentTypeName"),

    # getDepartmentTitle --> department_title
    ("bika_setup_catalog", "getDepartmentTitle"),

    # getPointOfCapture --> point_of_capture
    ("bika_setup_catalog", "getPointOfCapture"),

    # getDepartmentUID --> department_uid
    ("bika_setup_catalog", "getDepartmentUID"),

    # getCategoryUID --> category_uid
    ("bika_setup_catalog", "getCategoryUID"),

]

METADATA_TO_REMOVE = [
    # Not used anywhere. In SamplePoints and Specifications listings, the
    # SampleType object is waken-up instead of calling the metadata
    ("bika_setup_catalog", "getSampleTypeTitle"),

    # getSampleTypeUID (as metadata field) is only used for analyses and
    # samples (AnalysisRequest), and none of the two are stored in setup_catalog
    ("bika_setup_catalog", "getSampleTypeUID"),

    # Only used for when Sample and SamplePartition objects existed.
    # The following are the portal types stored in bika_catalog:
    #   Batch, BatchFolder and ReferenceSample
    # and "getSampleTypeTitle" metadata is not used for none of them
    ("bika_catalog", "getSampleTypeTitle"),

    # Not used anywhere
    ("bika_setup_catalog", "getAccredited"),

    # Not used anywhere
    ("bika_setup_catalog", "getBlank"),
    ("bika_setup_catalog", "getDuplicateVariation"),
    ("bika_setup_catalog", "getFormula"),
    ("bika_setup_catalog", "getInstrumentLocationName"),
    ("bika_setup_catalog", "getInstrumentTitle"),
    ("bika_setup_catalog", "getPrice"),
    ("bika_setup_catalog", "getTotalPrice"),
    ("bika_setup_catalog", "getVolume"),
    ("bika_setup_catalog", "getInstrumentTypeName"),
    ("bika_setup_catalog", "getInstrumentType"),
    ("bika_setup_catalog", "getHazardous"),
    ("bika_setup_catalog", "getManagerEmail"),
    ("bika_setup_catalog", "getManagerPhone"),
    ("bika_setup_catalog", "getManagerName"),
    ("bika_setup_catalog", "getMaxTimeAllowed"),
    ("bika_setup_catalog", "getModel"),
    ("bika_setup_catalog", "getCalculationTitle"),
    ("bika_setup_catalog", "getCalculationUID"),
    ("bika_setup_catalog", "getCalibrationExpiryDate"),
    ("bika_setup_catalog", "getDepartmentTitle"),
    ("bika_setup_catalog", "getVATAmount"),
    ("bika_setup_catalog", "getUnit"),
    ("bika_setup_catalog", "getPointOfCapture"),
    ("bika_setup_catalog", "getSamplePointUID"),
    ("bika_setup_catalog", "getFullname"),
    ("bika_setup_catalog", "cancellation_state"),
    ("bika_setup_catalog", "getName"),
    ("bika_setup_catalog", "getServiceUID"),
]


@upgradestep(product, version)
def upgrade(tool):
    portal = tool.aq_inner.aq_parent
    setup = portal.portal_setup
    ut = UpgradeUtils(portal)
    ver_from = ut.getInstalledVersion(product)

    if ut.isOlderVersion(product, version):
        logger.info("Skipping upgrade of {0}: {1} > {2}".format(
            product, ver_from, version))
        return True

    logger.info("Upgrading {0}: {1} -> {2}".format(product, ver_from, version))

    # -------- ADD YOUR STUFF BELOW --------

    # Fix Site Properties Generic Setup Export Step
    # https://github.com/senaite/senaite.core/pull/1469
    setup.runImportStepFromProfile(profile, "propertiestool")

    # Remove, rename and add indexes/metadata
    # https://github.com/senaite/senaite.core/pull/1486
    cleanup_indexes_and_metadata(portal)

    # Sample edit form (some selection widgets empty)
    # Reindex client's related fields (getClientUID, getClientTitle, etc.)
    # https://github.com/senaite/senaite.core/pull/1477
    reindex_client_fields(portal)

    # Redirect to worksheets folder when a Worksheet is removed
    # https://github.com/senaite/senaite.core/pull/1480
    setup_form_controller_actions(portal)

    logger.info("{0} upgraded to version {1}".format(product, version))
    return True


def reindex_client_fields(portal):
    logger.info("Reindexing client fields ...")
    fields_to_reindex = [
        "getClientUID",
        "getClientID",
        "getClientTitle",
        "getClientURL"
    ]

    # We only need to reindex those that might be associated to a Client object.
    # There is no need to reindex objects that already belong to a Client.
    # Batches were correctly indexed in previous upgrade step
    portal_types = [
        "AnalysisProfile",
        "AnalysisSpec",
        "ARTemplate",
        "SamplePoint"
    ]

    query = dict(portal_type=portal_types)
    brains = api.search(query, UID_CATALOG)
    total = len(brains)
    for num, brain in enumerate(brains):
        if num and num % 100 == 0:
            logger.info("Reindexing client fields: {}/{}".format(num, total))

        obj = api.get_object(brain)
        obj.reindexObject(idxs=fields_to_reindex)

    logger.info("Reindexing client fields ... [DONE]")

def cleanup_indexes_and_metadata(portal):
    # Remove stale indexes and metadata
    remove_stale_indexes(portal)
    remove_stale_metadata(portal)

    # Add new indexes
    add_new_indexes(portal)

    # Some indexes in setup_catalog changed
    reindex_labcontact_sortable_title(portal)
    reindex_supplier_manufacturers_titles(portal)


def reindex_labcontact_sortable_title(portal):
    logger.info("Reindexing sortable_title for LabContacts ...")
    query = dict(portal_type="LabContact")
    for brain in api.search(query, SETUP_CATALOG):
        obj = api.get_object(brain)
        obj.reindexObject(idxs=["sortable_title"])
    logger.info("Reindexing sortable_title for LabContacts ... [DONE]")


def reindex_supplier_manufacturers_titles(portal):
    logger.info("Reindexing title indexes for Suppliers and Manufacturers ...")
    query = dict(portal_type="Supplier")
    for brain in api.search(query, SETUP_CATALOG):
        obj = api.get_object(brain)
        obj.reindexObject(idxs=["title", "sortable_title"])
    logger.info("Reindexing title indexes for Suppliers and Manufacturers ... [DONE]")


def remove_stale_indexes(portal):
    logger.info("Removing stale indexes ...")
    for catalog, index in INDEXES_TO_REMOVE:
        del_index(catalog, index)
    logger.info("Removing stale indexes ... [DONE]")


def remove_stale_metadata(portal):
    logger.info("Removing stale metadata ...")
    for catalog, column in METADATA_TO_REMOVE:
        del_metadata(catalog, column)
    logger.info("Removing stale metadata ... [DONE]")


def del_index(catalog_id, index_name):
    logger.info("Removing '{}' index from '{}' ..."
                .format(index_name, catalog_id))
    catalog = api.get_tool(catalog_id)
    if index_name not in catalog.indexes():
        logger.info("Index '{}' not in catalog '{}' [SKIP]"
                    .format(index_name, catalog_id))
        return
    catalog.delIndex(index_name)


def del_metadata(catalog_id, column):
    logger.info("Removing '{}' metadata from '{}' ..."
                .format(column, catalog_id))
    catalog = api.get_tool(catalog_id)
    if column not in catalog.schema():
        logger.info("Metadata '{}' not in catalog '{}' [SKIP]"
                    .format(column, catalog_id))
        return
    catalog.delColumn(column)


def add_new_indexes(portal):
    logger.info("Adding new indexes ...")
    for catalog_id, index_name, index_metatype in INDEXES_TO_ADD:
        add_index(catalog_id, index_name, index_metatype)
    logger.info("Adding new indexes ... [DONE]")


def add_index(catalog_id, index_name, index_metatype):
    logger.info("Adding '{}' index to '{}' ...".format(index_name, catalog_id))
    catalog = api.get_tool(catalog_id)
    if index_name in catalog.indexes():
        logger.info("Index '{}' already in catalog '{}' [SKIP]"
                    .format(index_name, catalog_id))
        return
    catalog.addIndex(index_name, index_metatype)
    logger.info("Indexing new index '{}' ...".format(index_name))
    catalog.manage_reindexIndex(index_name)