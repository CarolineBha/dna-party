"""
Defining various networks
"""

import numpy as np

class NameIDMap:
    """
    Class for building a mapping, e.g., Actor name to id
    """

    def __init__(self, name):
        self.map = {}
        self.name = name

    def get_id(self, key_name):
        """
        Returns the id corresponding to the key_name provided
        """
        value = self.map.get(key_name, None)
        if isinstance(value, int):
            return value
        elif isinstance(value, dict):
            return value.get("id", None)
        else:
            return None 
    
    def build(self, name_list):
        """
        This function loops over a list and constructs a mapping dictionary
        """
        index = 0
        for element in name_list:

            if isinstance(element, tuple):
                name = element[0].strip()
                org = element[1]
            else:
                name = element.strip()

            found = self.map.get(name, None)
            if found is None:
                if isinstance(element, tuple):
                    self.map[name] = {"id": index, "party": org}
                else:
                    self.map[name] = index

                index += 1

    def get_len(self):
        """
        Return the size of the mapping dictionary
        """
        return len(self.map)
    
    def get_reverse_map(self):
        """
        Function returns a reverse mapping, i.e., from id to name
        """
        new_map = {}

        for k, v in self.map.items():
            if isinstance(v, int):
                new_map[v] = k
            else:
                new_map[v.get("id")] = {"name": k, "party": v.get("party")}
        
        return new_map


class StatementCount:
    """
    Class for preparing statement counts, all networks operate on this data
    3D Tensor,  dim 0 => actor
                dim 1 => concept
                dim 2 => qualifier
    """

    def __init__(self, verbose=True):
        self.verbose = verbose

    def build_data(self, data_frame, actor_var_name, cencept_var_name, qualifier_var_name, qualifier_values=None, add_field='party'):

        # Step 1: Getting the dimensions
        actor_map = NameIDMap('Actor')
        if add_field is not None:
            actor_map.build(zip(data_frame[actor_var_name], data_frame[add_field]))
        else:
            actor_map.build(data_frame[actor_var_name])

        n_actors = actor_map.get_len()

        concept_map = NameIDMap('Concept')
        concept_map.build(data_frame[cencept_var_name])
        n_concepts = concept_map.get_len()

        if qualifier_values is None:
            qualifier_values = np.unique(data_frame[qualifier_var_name])
        n_qualifier_levels = len(qualifier_values)

        if self.verbose:
            print('[*] Building statement data ...')
            print(f'\tNumber of actors = {n_actors}')
            print(f'\tNumber of concepts = {n_concepts}')
            print(f'\tNumber of qualifier levels = {n_qualifier_levels}')

        
        # Step 2: Allocating space for storing the 3D tensor
        data_count = np.zeros((n_actors, n_concepts, n_qualifier_levels), dtype=np.int32)

        # Step 3: Constructing data_count 
        for index, row in data_frame.iterrows():
            
            actor_id = actor_map.get_id(row[actor_var_name])
            concept_id = concept_map.get_id(row[cencept_var_name])

            assert actor_id is not None, 'Invalid actor found'  
            assert concept_id is not None, 'Invalid concept found'
            assert row[qualifier_var_name] >= 0, 'Index can not be negative'

            data_count[actor_id, concept_id, int(row[qualifier_var_name])] = 1

        return data_count, actor_map


class DiscourseNetworks(StatementCount):
    """
    Class for generating various discourse networks
    """

    def __init__(self, verbose=True):
        super().__init__(verbose=verbose)

    def get_actor_congruence_network(self, data_count, normalization='avg', min_concepts=2):
        """
        Computes the congruence metwork for the actors

        Parameters:
        -----------
            data_count : data_counts generated from dataframe
            normalization : The type of the normalization to use

        Returns:
        --------
            congruence_net : The congruence network of actors
        """
        n_actors = data_count.shape[0]

        congruence_net = np.zeros((n_actors, n_actors))

        for i in range(n_actors):
            for j in range(i):

                if normalization is None:
                    denom = 1
                elif normalization == 'avg':
                    denom = (np.sum(data_count[i]) + np.sum(data_count[j])) / 2
                elif normalization == 'cosine':
                    denom = np.sqrt(np.sum(data_count[i] ** 2)) * np.sqrt(np.sum(data_count[j] ** 2))
                else:
                    raise NotImplementedError(f"Normalization {normalization} not implemented") 

                score = np.sum(data_count[i] * data_count[j]) 
                if score >= min_concepts:
                    congruence_net[i, j] = score / denom
                    congruence_net[j, i] = congruence_net[i, j]

        return congruence_net


    def get_actor_conflict_network(self, data_count, normalization='avg', min_concepts=2):
        """
        Computes the conflict metwork for the actors

        Parameters:
        -----------
            data_count : data_counts generated from dataframe
            normalization : The type of the normalization to use

        Returns:
        --------
            conflict_net : The congruence network of actors
        """
        n_actors = data_count.shape[0]

        conflict_net = np.zeros((n_actors, n_actors))

        for i in range(n_actors):
            for j in range(i):

                if normalization is None:
                    denom = 1
                elif normalization == 'avg':
                    denom = (np.sum(data_count[i]) + np.sum(data_count[j])) / 2
                elif normalization == 'cosine':
                    denom = np.sqrt(np.sum(data_count[i] ** 2)) * np.sqrt(np.sum(data_count[j] ** 2))
                else:
                    raise NotImplementedError(f"Normalization {normalization} not implemented") 

                score = np.sum(data_count[i] * data_count[j][:,[1,0]])

                if score >= min_concepts:
                    conflict_net[i, j] = score / denom
                    conflict_net[j, i] = conflict_net[i, j]

        return conflict_net

    @staticmethod
    def get_degree_cetrality(adjacency_mat):

        edges = abs(adjacency_mat) > 0
        degrees = np.sum(edges, axis=0)
        max_degree = np.max(degrees)
        v = adjacency_mat.shape[0]

        graph_cetrality = np.sum(max_degree - degrees) / (v**2 - 3*v + 2)
        return graph_cetrality, max_degree
