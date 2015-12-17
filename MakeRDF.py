import os
import urllib.request
import re

class make_rdf:

    rdfs_value = '<http://www.w3.org/1999/02/22-rdf-syntax-ns#value>'
    rdfs_label = '<http://www.w3.org/2000/01/rdf-schema#label>'
    rdfs_subclass_of = '<http://www.w3.org/2000/01/rdf-schema#subClassOf>'
    xsd_string = '<http://www.w3.org/2001/XMLSchema#string>'
    xsd_float = '<http://www.w3.org/2001/XMLSchema#float>'

    usp_subject = '<http://www.m.u-tokyo.ac.jp/medinfo/rdf/usp/{:s}>'
    usp_predicate = '<http://www.m.u-tokyo.ac.jp/medinfo/rdf/usp#{:s}>'
    usp_graph = '<http://www.m.u-tokyo.ac.jp/medinfo/rdf/usp>'

    atc_subject = '<http://www.m.u-tokyo.ac.jp/medinfo/rdf/atc/{:s}>'
    atc_predicate = '<http://www.m.u-tokyo.ac.jp/medinfo/rdf/atc#{:s}>'
    atc_graph = '<http://www.m.u-tokyo.ac.jp/medinfo/rdf/atc>'

    kegg_subject = '<http://www.m.u-tokyo.ac.jp/medinfo/rdf/kegg/{:s}>'
    kegg_predicate = '<http://www.m.u-tokyo.ac.jp/medinfo/rdf/kegg#{:s}>'
    kegg_graph = '<http://www.m.u-tokyo.ac.jp/medinfo/rdf/kegg>'

    sider_subject = '<http://www.m.u-tokyo.ac.jp/medinfo/rdf/pubchem_compound:{:s}>'
    medis_subject = '<http://h.u-tokyo.ac.jp/medis/drug/{:s}>'

    def load_mapping(self, file_path):
        dic = {}
        for line in open(file_path, encoding='utf8'):
            array = line.strip().split('\t')
            kegg, medis = array[0], array[1]
            if kegg in dic:
                dic[kegg].append(medis)
            else:
                dic[kegg] = [medis]
        return dic

    def last_data_type(self, line, last_data_type):
        sline = line.strip()

        if sline.startswith('///'):
            last_data_type = '///'

        elif sline.startswith('ENTRY'):
            last_data_type = 'ENTRY'

        elif sline.startswith('NAME'):
            last_data_type = 'NAME'

        elif sline.startswith('FORMULA'):
            last_data_type = 'FORMULA'

        elif sline.startswith('EXACT_MASS'):
            last_data_type = 'EXACT_MASS'

        elif sline.startswith('MOL_WEIGHT'):
            last_data_type = 'MOL_WEIGHT'

        elif sline.startswith('ACTIVITY'):
            last_data_type = 'ACTIVITY'

        elif sline.startswith('REMARK'):
            last_data_type = 'REMARK'

        elif sline.startswith('INTERACTION'):
            last_data_type = 'INTERACTION'

        elif sline.startswith('BRITE'):
            last_data_type = 'BRITE'

        elif sline.startswith('TARGET'):
            last_data_type = 'TARGET'

        elif sline.startswith('PATHWAY'):
            last_data_type = 'PATHWAY'

        elif sline.startswith('DBLINKS'):
            last_data_type = 'DBLINKS'

        elif sline.startswith('ATOM'):
            last_data_type = 'ATOM'

        elif sline.startswith('BOND'):
            last_data_type = 'BOND'

        elif sline.startswith('COMPONENT'):
            last_data_type = 'COMPONENT'

        elif sline.startswith('SOURCE'):
            last_data_type = 'SOURCE'

        elif sline.startswith('SEQUENCE'):
            last_data_type = 'SEQUENCE'

        elif sline.startswith('COMMENT'):
            last_data_type = 'COMMENT'

        elif sline.startswith('TYPE'):
            last_data_type = 'TYPE'

        elif sline.startswith('BRACKET'):
            last_data_type = 'BRACKET'

        elif sline.startswith('ORIGINAL'):
            last_data_type = 'ORIGINAL'

        elif sline.startswith('REPEAT'):
            last_data_type = 'REPEAT'

        elif sline.startswith('METABOLISM'):
            last_data_type = 'METABOLISM'

        elif sline.startswith('STR_MAP'):
            last_data_type = 'STR_MAP'

        else:
            pass

        return last_data_type

    # Make KEGG-RDF
    def make_kegg(self, file_path):

        # LOAD KEGG-MEDIS MAPPING
        kegg2medis = self.load_mapping('./mapping/kegg-medis.tsv')
        kegg2usp = self.load_mapping('./mapping/kegg-usp.tsv')

        ld = ''
        triples = []

        kegg_main = open(file_path, encoding='utf8')

        for line in kegg_main:
            ld = self.last_data_type(line, ld)

            if ld is '///':
                pass

            elif ld is 'ENTRY':
                entry = re.search(r'D{1}\d{5}', line).group()
                # MAKE MAPPING to MEDIS
                if entry in kegg2medis:
                    for medis in kegg2medis[entry]:
                        triple = self.kegg_subject.format(entry) + ' ' + self.kegg_predicate.format('link_medis') + ' ' + self.medis_subject.format(medis) + ' ' + self.kegg_graph + ' .'
                        triples.append(triple)

                # MAKE MAPPING to USP
                if entry in kegg2usp:
                    for usp in kegg2usp[entry]:
                        triple = self.kegg_subject.format(entry) + ' ' + self.kegg_predicate.format('link_usp') + ' ' + self.usp_subject.format(usp) + ' ' + self.kegg_graph + ' .'
                        triples.append(triple)

            elif ld is 'NAME':
                val = line.replace(ld, '').replace('"', "'").strip()
                triple = self.kegg_subject.format(entry) + ' ' + self.kegg_predicate.format(ld.lower()) + ' "' + val + '"^^' + self.xsd_string + ' ' + self.kegg_graph + ' .'
                triples.append(triple)

            elif ld is 'FORMULA':
                val = line.replace(ld, '').replace('"', "'").strip()
                triple = self.kegg_subject.format(entry) + ' ' + self.kegg_predicate.format(ld.lower()) + ' "' + val + '"^^' + self.xsd_string + ' ' + self.kegg_graph + ' .'
                triples.append(triple)

            elif ld is 'EXACT_MASS':
                val = line.replace(ld, '').replace('"', "'").strip()
                triple = self.kegg_subject.format(entry) + ' ' + self.kegg_predicate.format(ld.lower()) + ' "' + val + '"^^' + self.xsd_float + ' ' + self.kegg_graph + ' .'
                triples.append(triple)

            elif ld is 'MOL_WEIGHT':
                val = line.replace(ld, '').replace('"', "'").strip()
                triple = self.kegg_subject.format(entry) + ' ' + self.kegg_predicate.format(ld.lower()) + ' "' + val + '"^^' + self.xsd_float + ' ' + self.kegg_graph + ' .'
                triples.append(triple)

            elif ld is 'ACTIVITY':
                val = line.replace(ld, '').replace('"', "'").strip()
                triple = self.kegg_subject.format(entry) + ' ' + self.kegg_predicate.format(ld.lower()) + ' "' + val + '"^^' + self.xsd_string + ' ' + self.kegg_graph + ' .'
                triples.append(triple)

            elif ld is 'REMARK':
                val = line.replace(ld, '').strip()
                if val.startswith('ATC code: '):
                    atc_codes = val.replace('ATC code: ', '').split(' ')
                    for atc_code in atc_codes:
                        triple = self.kegg_subject.format(entry) + ' ' + self.kegg_predicate.format('link_atc') + ' ' + self.atc_subject.format(atc_code) + ' ' + self.kegg_graph + ' .'
                        triples.append(triple)

            elif ld is 'INTERACTION':
                pass

            elif ld is 'BRITE':
                pass

            elif ld is 'TARGET':
                val = line.replace(ld, '').replace('"', "'").strip()
                triple = self.kegg_subject.format(entry) + ' ' + self.kegg_predicate.format(ld.lower()) + ' "' + val + '"^^' + self.xsd_string + ' ' + self.kegg_graph + ' .'
                triples.append(triple)

            elif ld is 'PATHWAY':
                val = '_'.join(line.replace(ld, '').strip().split('  '))
                triple = self.kegg_subject.format(entry) + ' ' + self.kegg_predicate.format(ld.lower()) + ' "' + val + '"^^' + self.xsd_string + ' ' + self.kegg_graph + ' .'
                triples.append(triple)

            elif ld is 'DBLINKS':
                pass

            elif ld is 'ATOM':
                pass

            elif ld is 'BOND':
                pass

            elif ld is 'COMPONENT':
                val = line.replace(ld, '').replace('(', '').replace(')', '').replace('|', ',').strip().split(',')
                for x in val:
                    x = x.strip()
                    if re.match(r'.*\[.+\]', x):
                        triple = self.kegg_subject.format(entry) + ' ' + self.kegg_predicate.format(ld.lower()) + ' "' + x + '"^^' + self.xsd_string + ' ' + self.kegg_graph + ' .'
                        triples.append(triple)

            elif ld is 'SOURCE':
                val = line.replace(ld, '').replace(';', ',').replace('"', "'").strip().split(',')
                for x in val:
                    x = x.strip()
                    triple = self.kegg_subject.format(entry) + ' ' + self.kegg_predicate.format(ld.lower()) + ' "' + x + '"^^' + self.xsd_string + ' ' + self.kegg_graph + ' .'
                    triples.append(triple)

            elif ld is 'SEQUENCE':
                pass

            elif ld is 'COMMENT':
                pass

            elif ld is 'TYPE':
                pass

            elif ld is 'BRACKET':
                pass

            elif ld is 'ORIGINAL':
                pass

            elif ld is 'REPEAT':
                pass

            elif ld is 'METABOLISM':
                val = line.replace(ld, '').lstrip()

                if val.startswith('Enzyme:'):
                    predicate = self.kegg_predicate.format(ld.lower() + '_' + 'Enzyme'.lower())
                    val = val.replace('Enzyme:', '').split(',')
                elif val.startswith('Transporter:') or val.startswith('Transpoter:'):
                    predicate = self.kegg_predicate.format(ld.lower() + '_' + 'Transporter'.lower())
                    val = val.replace('Transporter:', '').split(',')
                elif val.startswith('Metabolism:'):
                    predicate = self.kegg_predicate.format(ld.lower() + '_' + 'Metabolism'.lower())
                    val = val.replace('Metabolism:', '').split(',')
                else:
                    predicate = self.kegg_predicate.format(ld.lower() + '_' + 'Others'.lower())
                    val = val.split(',')

                for x in val:
                    x = x.strip()
                    triple = self.kegg_subject.format(entry) + ' ' + predicate + ' "' + x + '"^^' + self.xsd_string + ' ' + self.kegg_graph + ' .'
                    triples.append(triple)

        return triples

    # Make ATC-RDF
    def make_atc(self, file_path):

        atc2sider = self.load_mapping('./mapping/atc-sider.tsv')

        level_ROOT, level_A, level_B, level_C, level_D, level_E  = 'ROOT', '', '', '', '', ''
        triples = []

        kegg_atc = open(file_path, encoding='utf8')
        for line in kegg_atc:

            if line.startswith('A'):
                line = line.strip()
                entry = line[0:2]
                label = line[3:len(line)]
                level_A = entry

                triple_1 = self.atc_subject.format(entry) + ' ' + self.rdfs_label       + ' ' + '"' + label + '"@en ' + self.atc_graph + ' .'
                triple_2 = self.atc_subject.format(entry) + ' ' + self.rdfs_value       + ' ' + '"' + entry + '" '    + self.atc_graph + ' .'
                triple_3 = self.atc_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.atc_subject.format(level_ROOT) + ' ' + self.atc_graph + ' .'

                triples.append(triple_1)
                triples.append(triple_2)
                triples.append(triple_3)

            elif line.startswith('B'):
                line = line.replace('B  ', '').strip()
                entry = line[0:3]
                label = line[4:len(line)]
                level_B = entry

                triple_1 = self.atc_subject.format(entry) + ' ' + self.rdfs_label       + ' ' + '"' + label + '"@en ' + self.atc_graph + ' .'
                triple_2 = self.atc_subject.format(entry) + ' ' + self.rdfs_value       + ' ' + '"' + entry + '" '    + self.atc_graph + ' .'
                triple_3 = self.atc_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.atc_subject.format(level_ROOT) + ' ' + self.atc_graph + ' .'
                triple_4 = self.atc_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.atc_subject.format(level_A) + ' ' + self.atc_graph + ' .'

                triples.append(triple_1)
                triples.append(triple_2)
                triples.append(triple_3)
                triples.append(triple_4)

            elif line.startswith('C'):
                line = line.replace('C    ', '').strip()
                entry = line[0:4]
                label = line[5:len(line)]
                level_C = entry

                triple_1 = self.atc_subject.format(entry) + ' ' + self.rdfs_label       + ' ' + '"' + label + '"@en ' + self.atc_graph + ' .'
                triple_2 = self.atc_subject.format(entry) + ' ' + self.rdfs_value       + ' ' + '"' + entry + '" '    + self.atc_graph + ' .'
                triple_3 = self.atc_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.atc_subject.format(level_ROOT) + ' ' + self.atc_graph + ' .'
                triple_4 = self.atc_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.atc_subject.format(level_A) + ' ' + self.atc_graph + ' .'
                triple_5 = self.atc_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.atc_subject.format(level_B) + ' ' + self.atc_graph + ' .'

                triples.append(triple_1)
                triples.append(triple_2)
                triples.append(triple_3)
                triples.append(triple_4)
                triples.append(triple_5)

            elif line.startswith('D'):
                line = line.replace('D      ', '').strip()
                entry = line[0:5]
                label = line[6:len(line)].strip()
                level_D = entry

                triple_1 = self.atc_subject.format(entry) + ' ' + self.rdfs_label       + ' ' + '"' + label + '"@en ' + self.atc_graph + ' .'
                triple_2 = self.atc_subject.format(entry) + ' ' + self.rdfs_value       + ' ' + '"' + entry + '" '    + self.atc_graph + ' .'
                triple_3 = self.atc_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.atc_subject.format(level_ROOT) + ' ' + self.atc_graph + ' .'
                triple_4 = self.atc_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.atc_subject.format(level_A) + ' ' + self.atc_graph + ' .'
                triple_5 = self.atc_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.atc_subject.format(level_B) + ' ' + self.atc_graph + ' .'
                triple_6 = self.atc_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.atc_subject.format(level_C) + ' ' + self.atc_graph + ' .'

                triples.append(triple_1)
                triples.append(triple_2)
                triples.append(triple_3)
                triples.append(triple_4)
                triples.append(triple_5)
                triples.append(triple_6)

            elif line.startswith('E'):
                line = line.replace('E        ', '').strip()
                entry = line[0:7]
                label = line[8:len(line)].strip()

                level_E = entry

                triple_1 = self.atc_subject.format(entry) + ' ' + self.rdfs_label       + ' ' + '"' + label + '"@en ' + self.atc_graph + ' .'
                triple_2 = self.atc_subject.format(entry) + ' ' + self.rdfs_value       + ' ' + '"' + entry + '" '    + self.atc_graph + ' .'
                triple_3 = self.atc_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.atc_subject.format(level_ROOT) + ' ' + self.atc_graph + ' .'
                triple_4 = self.atc_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.atc_subject.format(level_A) + ' ' + self.atc_graph + ' .'
                triple_5 = self.atc_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.atc_subject.format(level_B) + ' ' + self.atc_graph + ' .'
                triple_6 = self.atc_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.atc_subject.format(level_C) + ' ' + self.atc_graph + ' .'
                triple_7 = self.atc_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.atc_subject.format(level_D) + ' ' + self.atc_graph + ' .'

                triples.append(triple_1)
                triples.append(triple_2)
                triples.append(triple_3)
                triples.append(triple_4)
                triples.append(triple_5)
                triples.append(triple_6)
                triples.append(triple_7)

                # MAKE MAPPING to SIDER
                if entry in atc2sider:
                    for sider in atc2sider[entry]:
                        triple = self.atc_subject.format(entry) + ' ' + self.atc_predicate.format('link_sider') + ' ' + self.sider_subject.format(sider) + ' ' + self.atc_graph + ' .'
                        triples.append(triple)

            elif line.startswith('F'):
                line = line.replace('F          ', '').strip()
                entry = line[0:6]

                if re.match(r'D{1}\d{5}', entry):
                    triple_1 = self.atc_subject.format(level_E) + ' ' + self.atc_predicate.format('link_kegg') + ' ' + self.kegg_subject.format(entry) + ' ' + self.atc_graph + ' .'
                    triples.append(triple_1)

        return triples

    # MAKE USP-RDF
    def make_usp(self, file_path):

        level_ROOT, level_A, level_B, level_C, level_D = 'ROOT', '', '', '', ''
        triples = []

        kegg_usp = open(file_path, encoding='utf8')
        for line in kegg_usp:

            if line.startswith('A'):
                line = line.strip()
                entry = line[1:len(line)].replace(' ', '_').replace('/', '_')
                label = line[1:len(line)].replace('"', "'")
                level_A = entry

                triple_1 = self.usp_subject.format(entry) + ' ' + self.rdfs_label       + ' ' + '"' + label + '"^^' + self.xsd_string + ' ' + self.usp_graph + ' .'
                triple_2 = self.usp_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.usp_subject.format(level_ROOT) + ' ' + self.usp_graph + ' .'

                triples.append(triple_1)
                triples.append(triple_2)

            elif line.startswith('B'):
                line = line.replace('B  ', '').strip()
                entry = line[0:len(line)].replace(' ', '_').replace('/', '_')
                label = line[0:len(line)].replace('"', "'")
                level_B = entry

                triple_1 = self.usp_subject.format(entry) + ' ' + self.rdfs_label       + ' ' + '"' + label + '"^^' + self.xsd_string + ' ' + self.usp_graph + ' .'
                triple_2 = self.usp_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.usp_subject.format(level_ROOT) + ' ' + self.usp_graph + ' .'
                triple_3 = self.usp_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.usp_subject.format(level_A) + ' ' + self.usp_graph + ' .'

                triples.append(triple_1)
                triples.append(triple_2)
                triples.append(triple_3)

            elif line.startswith('C'):
                line = line.replace('C    ', '').strip()

                if re.match(r'D{1}\d{5}', line[0:6]):
                    # Link to KEGG
                    entry = line[0:6]
                    triple_1 = self.usp_subject.format(level_B) + ' ' + self.usp_predicate.format('link_kegg') + ' ' + self.kegg_subject.format(entry) + ' ' + self.usp_graph + ' .'
                    triples.append(triple_1)
                else:
                    entry = line[0:len(line)].replace(' ', '_').replace('/', '_')
                    label = line[0:len(line)].replace('"', "'")
                    level_C = entry

                    triple_1 = self.usp_subject.format(entry) + ' ' + self.rdfs_label       + ' ' + '"' + label + '"^^' + self.xsd_string + ' ' + self.usp_graph + ' .'
                    triple_2 = self.usp_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.usp_subject.format(level_ROOT) + ' ' + self.usp_graph + ' .'
                    triple_3 = self.usp_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.usp_subject.format(level_A) + ' ' + self.usp_graph + ' .'
                    triple_4 = self.usp_subject.format(entry) + ' ' + self.rdfs_subclass_of + ' ' + self.usp_subject.format(level_B) + ' ' + self.usp_graph + ' .'

                    triples.append(triple_1)
                    triples.append(triple_2)
                    triples.append(triple_3)
                    triples.append(triple_4)


            elif line.startswith('D'):
                line = line.replace('D      ', '').strip()
                if re.match(r'D{1}\d{5}', line[0:6]):
                    # Link to KEGG
                    entry = line[0:6]
                    triple_1 = self.usp_subject.format(level_C) + ' ' + self.usp_predicate.format('link_kegg') + ' ' + self.kegg_subject.format(entry) + ' ' + self.usp_graph + ' .'
                    triples.append(triple_1)

        return triples

if __name__ == '__main__':
    make_rdf = make_rdf()

    ## MAKE USP-RDF FROM KEGG SITE
    if os.path.exists('./rdf/usp_201512.nq'):
        print ('RDF file for USP already exist.')
    else:
        if not os.path.exists('./br08302.keg'):
            url = 'http://www.genome.jp/kegg-bin/download_htext?htext=br08302.keg&format=htext&filedir='
            print('File for USP not exists. Downloading from {:s}'.format(url))
            url_obj = urllib.request.urlopen(url)
            local = open(os.path.basename('br08302.keg'), 'wb')
            local.write(url_obj.read())
            url_obj.close()
            local.close()
            print ('Fetch br08302.keg done.')
        else:
            print ('File for USP already exist.')

        print ('Make USP-RDF File.')
        triples = make_rdf.make_usp('./br08302.keg')
        out = open('./rdf/usp_201512.nq', 'w', encoding='utf8')
        for line in triples:
            out.write(line + '\n')
            out.flush()
        out.close()
        print ('Done.')

    ## MAKE ATC-RDF FROM KEGG SITE
    if os.path.exists('./rdf/atc_201512.nq'):
        print ('RDF file for ATC already exist.')
    else:
        if not os.path.exists('./br08303.keg'):
            url = 'http://www.genome.jp/kegg-bin/download_htext?htext=br08303.keg&format=htext&filedir='
            print('File for ATC not exists. Downloading from {:s}'.format(url))
            url_obj = urllib.request.urlopen(url)
            local = open(os.path.basename('br08303.keg'), 'wb')
            local.write(url_obj.read())
            url_obj.close()
            local.close()
            print ('Fetch br08303.keg done.')
        else:
            print ('File for ATC already exist.')

        print ('Make ATC-RDF File.')
        triples = make_rdf.make_atc('./br08303.keg')
        out = open('./rdf/atc_201512.nq', 'w', encoding='utf8')
        for line in triples:
            out.write(line + '\n')
            out.flush()
        out.close()
        print ('Done.')

    ## MAKE KEGG-RDF FROM KEGG SITE
    if os.path.exists('./rdf/kegg_201512.nq'):
        print ('RDF file for KEGG already exist.')
    else:
        if not os.path.exists('./drug'):
            url = 'ftp://ftp.genome.jp/pub/kegg/medicus/drug/drug'
            print('File for KEGG not exists. Downloading from {:s}'.format(url))
            print ('This may take several minutes...')
            url_obj = urllib.request.urlopen(url)
            local = open(os.path.basename('drug'), 'wb')
            local.write(url_obj.read())
            url_obj.close()
            local.close()
            print ('Fetch drug done.')
        else:
            print ('File for KEGG already exist.')

        print ('Make KEGG-RDF File.')
        triples = make_rdf.make_kegg('./drug')
        out = open('./rdf/kegg_201512.nq', 'w', encoding='utf8')
        for line in triples:
            out.write(line + '\n')
            out.flush()
        out.close()
        print ('Done.')
