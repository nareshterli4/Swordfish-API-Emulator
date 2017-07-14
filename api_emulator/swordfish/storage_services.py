# Copyright Notice:SNIA
# Copyright 2017 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Storage Services Module


import json, os
import traceback
import urllib2

from flask import jsonify, request
from flask.ext.restful import Resource

from constants import *


class StorageServicesCollectionAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']

    def get(self):
        path = '{}{}{}'.format(self.root, self.storage_services, 'index.json')
        try:
            storage_services_json = open(path)
            data = json.load(storage_services_json)
        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self):
        pass

    def delete(self):
        pass


class StorageServicesAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']

    def get(self, storage_service):
        path = '{}{}{}/{}'.format(self.root, self.storage_services, storage_service, 'index.json')
        print("StorageServicesAPI--Path---{}".format(path))
        try:
            storage_service_json = open(path)
            data = json.load(storage_service_json)
        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self):
        pass

    def delete(self):
        pass


class StorageGroupsCollectionAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.storage_groups = PATHS['StorageServices']['storage_groups']

    def get(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                    self.storage_groups, 'index.json')
        print("StorageGroupsCollectionAPI--Path---{}".format(path))
        list_of_keys = ['Description', 'Members', 'Name', 'Oem','Permissions']
        key_values = {
	    'Permissions': ['@odata.id'],
            'Members': ['@odata.id', 'AccessState', 'Actions', 'ClientEndpointGroups', 'Description', 'Id', 'Identifier',
                        'Links', 'MembersAreConsistent', 'Name', 'Oem', 'ReplicaInfos', 'ServerEndpointGroups',
                        'Status', 'VolumesAreExposed']
        }
        try:
            storage_groups_json = open(path)
            data = json.load(storage_groups_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if key == 'Members' and 'Members' in data:
                    data['Members'] = [{k: v for k, v in member.items()
                                        if k in key_values['Members']}
                                       for member in data['Members']]

        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self):
        pass

    def delete(self):
        pass


class StorageGroupsAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.storage_groups = PATHS['StorageServices']['storage_groups']

    def get(self, storage_service, storage_group):
        path = '{}{}{}/{}{}/{}'.format(self.root, self.storage_services, storage_service,
                                       self.storage_groups, storage_group, 'index.json')
        list_of_keys = ['AccessState', 'Actions', 'ClientEndpointGroups', 'Description', 'Id', 'Identifier', 'Links',
                        'MembersAreConsistent', 'Name', 'Oem', 'ReplicaInfos', 'ServerEndpointGroups',
                        'Status', 'Volumes', 'VolumesAreExposed']
        key_values = {
            'Actions': ['#StorageGroup.v1_0_0.ExposeVolumes', '#StorageGroup.v1_0_0.HideVolumes', 'Oem'],
            'Links': ['ChildStorageGroups', 'ClassOfService', 'Oem', 'ParentStorageGroups'],
            'ReplicaInfos': ['ConsistencyEnabled', 'ConsistencyState', 'ConsistencyStatus',
                             'ConsistencyType', 'FailedCopyStopsHostIO', 'PercentSynced', 'Replica',
                             'ReplicaPriority', 'ReplicaProgressStatus', 'ReplicaReadOnlyAccess',
                             'ReplicaRecoveryMode', 'ReplicaRole', 'ReplicaSkewBytes',
                             'ReplicaState', 'ReplicaType', 'ReplicaUpdateMode',
                             'RequestedReplicaState', 'SyncMaintained', 'UndiscoveredElement',
                             'WhenActivated', 'WhenDeactivated', 'WhenEstablished', 'WhenSuspended',
                             'WhenSynced', 'WhenSynchronized'],
            'Volumes': ['Description', 'Members', 'Name', 'Oem']
        }

        try:
            storage_groups_json = open(path)
            data = json.load(storage_groups_json)
            data = {key: data[key] for key in list_of_keys if key in data.keys()}
            for key, value in data.items():
                # if key not in list_of_keys:
                #     del data[key]
                #     continue
                if key == 'Actions' and 'Actions' in data:
                    data['Actions'] = {k: v for k, v in data['Actions'].items() if k in key_values['Actions']}

                if key == 'Links' and 'Links' in data:
                    data['Links'] = {k: v for k, v in data['Links'].items() if k in key_values['Links']}

                if type(data.get('Volumes')) is list:
                    
                    data['Volumes'] = [{k: v for k, v in volumes.items()
                                               if k in key_values['Volumes']}
                                              for volumes in data['Volumes']]
                             
                elif data.get('Volumes'):
                    
                    data['Volumes'] = {k: v for k, v in data['Volumes'].items()
                                               if k in key_values['Volumes']}

                if key == 'ReplicaInfos' and 'ReplicaInfos' in data:
                    data['ReplicaInfos'] = [{k: v for k, v in replicainfo.items() if k in key_values['ReplicaInfos']}
                                            for replicainfo in data['ReplicaInfos']]

        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self):
        pass

    def delete(self):
        pass


class StoragePoolsCollectionAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.storage_pools = PATHS['StorageServices']['storage_pools']

    def get(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                    self.storage_pools, 'index.json')
        print("StoragePoolsCollectionAPI--Path---{}".format(path))
        list_of_keys = ['Description', 'Members', 'Name', 'Oem','Permissions']
        key_values = {
	    'Permissions': ['@odata.id'],
            'Members': ['@odata.id', 'AllocatedPools', 'AllocatedVolumes', 'BlockSizeBytes', 'Capacity', 'CapacitySources',
                        'ClassesOfService', 'Description', 'Id', 'Identifier', 'Links',
                        'LowSpaceWarningThresholdPercents', 'Name', 'Oem', 'Status'],
        }
        try:
            storage_pools_json = open(path)
            data = json.load(storage_pools_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if key == 'Members' and 'Members' in data:
                    data['Members'] = [{k: v for k, v in member.items()
                                        if k in key_values['Members']}
                                       for member in data['Members']]

        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self):
        pass

    def delete(self):
        pass


class StoragePoolsAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.storage_pools = PATHS['StorageServices']['storage_pools']

    def get(self, storage_service, storage_pool):
       # import pdb; pdb.set_trace()
        path = '{}{}{}/{}{}/{}'.format(self.root, self.storage_services, storage_service,
                                       self.storage_pools, storage_pool, 'index.json')
        list_of_keys = ['AllocatedPools', 'AllocatedVolumes', 'BlockSizeBytes', 'Capacity', 'CapacitySources',
                        'ClassesOfService', 'Description', 'Id', 'Identifier', 'Links',
                        'LowSpaceWarningThresholdPercents', 'Name', 'Oem', 'Status']
        key_values = {
            'AllocatedPools': ['Description', 'Members', 'Name', 'Oem'],
            'AllocatedVolumes': ['Description', 'Members', 'Name', 'Oem'],
            'Capacity': ['Data', 'IsThinProvisioned', 'Metadata', 'Snapshot'],
            'CapacitySources': ['ProvidedCapacity', 'ProvidedClassOfService', 'ProvidingDrives', 'ProvidingPools',
                                'ProvidingVolumes', 'LowSpaceWarningThresholdPercents'],
            'ClassesOfService': ['Description', 'Members', 'Name', 'Oem'],
            'Links': ['DefaultClassOfService', 'Oem'],
        }
        try:
            storage_pools_json = open(path)
            data = json.load(storage_pools_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if key == 'AllocatedPools' and 'AllocatedPools' in data:
                    data['AllocatedPools'] = [{k: v for k, v in alloted_pools.items()
                                               if k in key_values['AllocatedPools']}
                                              for alloted_pools in data['AllocatedPools']]
                if key == 'AllocatedVolumes' and 'AllocatedVolumes' in data:
                    data['AllocatedVolumes'] = {k: v for k, v in data['AllocatedVolumes'].items()
                                                if k in key_values['AllocatedVolumes']}

                if type(data.get('Capacity')) is list:                    
                    data['Capacity'] = [{k: v for k, v in capacity.items()
                                               if k in key_values['Capacity']}
                                              for capacity in data['Capacity']]
                elif data.get('Capacity'):                    
                    data['Capacity'] = {k: v for k, v in data['Capacity'].items()
                                               if k in key_values['Capacity']}

                if key == 'CapacitySources' and 'CapacitySources' in data:
                    data['CapacitySources'] = [{k: v for k, v in capacity_source.items()
                                                if k in key_values['CapacitySources']}
                                               for capacity_source in data['CapacitySources']]

                if type(data.get('ClassesOfService')) is list:                    
                    data['ClassesOfService'] = [{k: v for k, v in classesofservice.items()
                                               if k in key_values['ClassesOfService']}
                                              for classesofservice in data['ClassesOfService']]
                elif data.get('ClassesOfService'):                    
                    data['ClassesOfService'] = {k: v for k, v in data['ClassesOfService'].items()
                                               if k in key_values['ClassesOfService']}

                if key == 'Links' and 'Links' in data:
                    data['Links'] = {k: v for k, v in data['Links'].items() if k in key_values['Links']}

        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self):
        pass

    def delete(self):
        pass




class StoragePoolChildAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.storage_pools = PATHS['StorageServices']['storage_pools']

    def get(self, storage_service, storage_pool, values):
        path = '{}{}{}/{}{}/{}/{}'.format(self.root, self.storage_services, storage_service,
                                       self.storage_pools, storage_pool, values, 'Index.json')

        try:
            storage_pools_child_json = open(path)
            data = json.load(storage_pools_child_json)
        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)




class ClientEndpointGroupsCollectionAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.client_end_point_groups = PATHS['StorageServices']['client_end_point_groups']

    def get(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                    self.client_end_point_groups, 'Index.json')
        print("ClientEndpointGroupsCollectionAPI--Path---{}".format(path))
        list_of_keys = ['AccessState', 'Description', 'Endpoints', 'GroupType', 'Id', 'Identifier', 'Links',
                        'Name', 'Oem', 'Preferred', 'TargetEndpointGroupIdentifier','Permissions']
        key_values = {
	    'Permissions': ['@odata.id'],
            'Endpoints': ['Description', 'Members', 'Name', 'Oem']
        }
        try:
            client_end_point_groups = open(path)
            data = json.load(client_end_point_groups)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if key == 'Endpoints' and 'Endpoints' in data:
                    data['Endpoints'] = {k: v for k, v in data['Endpoints'].items() if k in key_values['Endpoints']}

        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)
		
    def put(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                       self.client_end_point_group, 'index.json')
        try:
            # Read json from file.
            with open(path, 'r') as client_end_point_group_json:
                data = json.load(client_end_point_group_json)
                client_end_point_group_json.close()

            request_data = json.loads(request.data)

            if request_data:
                # Update the keys of payload in json file.
                for key, value in request_data.items():
                    if key in data and data[key]:
                        data[key] = value

            # Write the updated json to file.
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        json_data = self.get(storage_service)
        return json_data


class ClientEndpointGroupsAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.client_end_point_groups = PATHS['StorageServices']['client_end_point_groups']

    def get(self, storage_service, client_end_point_group):
        path = '{}{}{}/{}{}/{}'.format(self.root, self.storage_services, storage_service,
                                       self.client_end_point_groups, client_end_point_group, 'index.json')
        list_of_keys = ['AccessState', 'Description', 'Endpoints', 'GroupType', 'Id', 'Identifier', 'Links',
                        'Name', 'Oem', 'Preferred', 'TargetEndpointGroupIdentifier']
        key_values = {
            'Endpoints': ['Description', 'Members', 'Name', 'Oem']
        }

        try:
            #import ipdb; ipdb.set_trace()
            client_end_point_groups_json = open(path)
            data = json.load(client_end_point_groups_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if key == 'Endpoints' and 'Endpoints' in data:
                    data['Endpoints'] = {k: v for k, v in data['Endpoints'].items() if k in key_values['Endpoints']}

        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self, storage_service, client_end_point_group):
        path = '{}{}{}/{}{}/{}'.format(self.root, self.storage_services, storage_service,
                                       self.client_end_point_group, client_end_point_group, 'index.json')
        try:
            # Read json from file.
            with open(path, 'r') as client_end_point_group_json:
                data = json.load(client_end_point_group_json)
                client_end_point_group_json.close()

            request_data = json.loads(request.data)

            if request_data:
                # Update the keys of payload in json file.
                for key, value in request_data.items():
                    if key in data and data[key]:
                        data[key] = value

            # Write the updated json to file.
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        json_data = self.get(storage_service, client_end_point_group)
        return json_data

    def delete(self):
        pass


class ServerEndpointGroupsCollectionAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.server_end_point_groups = PATHS['StorageServices']['server_end_point_groups']

    def get(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                    self.server_end_point_groups, 'Index.json')
        print("ServerEndpointGroupsCollectionAPI--Path---{}".format(path))

        list_of_keys = ['AccessState', 'Description', 'Endpoints', 'GroupType', 'Id', 'Identifier', 'Links',
                        'Name', 'Oem', 'Preferred', 'TargetEndpointGroupIdentifier','Permissions']
        key_values = {
	    'Permissions': ['@odata.id'],
            'Endpoints': ['Description', 'Members', 'Name', 'Oem']
        }

        try:
            server_end_point_groups = open(path)
            data = json.load(server_end_point_groups)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if key == 'Endpoints' and 'Endpoints' in data:
                    data['Endpoints'] = {k: v for k, v in data['Actions'].items() if k in key_values['Endpoints']}

        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)
		
	def put(self, storage_service):
		path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                       self.server_end_point_group, 'index.json')
        try:
            # Read json from file.
            with open(path, 'r') as server_end_point_group_json:
                data = json.load(server_end_point_group_json)
                server_end_point_group_json.close()

            request_data = json.loads(request.data)

            if request_data:
                # Update the keys of payload in json file.
                for key, value in request_data.items():
                    if key in data and data[key]:
                        data[key] = value

            # Write the updated json to file.
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        json_data = self.get(storage_service)
        return json_data


class ServerEndpointGroupsAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.server_end_point_groups = PATHS['StorageServices']['server_end_point_groups']

    def get(self, storage_service, server_end_point_group):
        path = '{}{}{}/{}{}/{}'.format(self.root, self.storage_services, storage_service,
                                       self.server_end_point_groups, server_end_point_group,'Index.json')
        list_of_keys = ['AccessState', 'Description', 'Endpoints', 'GroupType', 'Id', 'Identifier', 'Links',
                        'Name', 'Oem', 'Preferred', 'TargetEndpointGroupIdentifier']
        key_values = {
            'Endpoints': ['Description', 'Members', 'Name', 'Oem']
        }

        try:
            server_end_point_groups = open(path)
            data = json.load(server_end_point_groups)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if key == 'Endpoints' and 'Endpoints' in data:
                    data['Endpoints'] = {k: v for k, v in data['Actions'].items() if k in key_values['Endpoints']}

        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self, storage_service, server_end_point_group):
        path = '{}{}{}/{}{}/{}'.format(self.root, self.storage_services, storage_service,
                                       self.server_end_point_group, server_end_point_group, 'index.json')
        try:
            # Read json from file.
            with open(path, 'r') as server_end_point_group_json:
                data = json.load(server_end_point_group_json)
                server_end_point_group_json.close()

            request_data = json.loads(request.data)

            if request_data:
                # Update the keys of payload in json file.
                for key, value in request_data.items():
                    if key in data and data[key]:
                        data[key] = value

            # Write the updated json to file.
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        json_data = self.get(storage_service, server_end_point_group)
        return json_data

    def delete(self):
        pass


class DrivesCollectionAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.drives = PATHS['StorageServices']['drives']

    def get(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                    self.drives, 'Index.json')
        print("DrivesCollectionAPI--Path---{}".format(path))
        list_of_keys = ['Description', 'Members', 'Name', 'Oem','Permissions']
	key_values = {
	    'Permissions': ['@odata.id'],
           }
        try:
            drives = open(path)
            data = json.load(drives)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue

        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)


class DrivesAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.drives = PATHS['StorageServices']['drives']

    def get(self, storage_service, drive):
        path = '{}{}{}/{}{}/{}'.format(self.root, self.storage_services, storage_service,
                                       self.drives, drive, 'index.json')
        list_of_keys = ['Description', 'Members', 'Name', 'Oem']

        try:
            drive = open(path)
            data = json.load(drive)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self):
        pass

    def delete(self):
        pass


##########################################################




class ClassesOfServiceChildAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.classes_of_service = PATHS['StorageServices']['class_of_service']

    def get(self, storage_service, classes_of_service, value):
        path = '{}{}{}/{}{}/{}/{}'.format(self.root, self.storage_services, storage_service,
                                       self.classes_of_service, classes_of_service, values, 'index.json')

        try:
            classes_of_service_json = open(path)
            data = json.load(classes_of_service_json)
        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)





class ClassesOfServiceAPI(Resource):
    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.classes_of_service = PATHS['StorageServices']['class_of_service']

    def get(self, storage_service, classes_of_service):
        path = '{}{}{}/{}{}/{}'.format(self.root, self.storage_services, storage_service,
                                       self.classes_of_service, classes_of_service, 'index.json')
        list_of_keys = ['ClassOfServiceVersion', 'Description', 'Id', 'Identifier', 'LinesOfService', 'Name', 'Oem']
        key_values = {
            'LinesOfService': ['@odata.id','IOPerformanceLineOfService', 'IOConnectivityLineOfService', 'DataStorageLineOfService',
                               'DataSecurityLineOfService', 'DataProtectionLineOfService']

        }
        try:
            classes_of_service_json = open(path)
            data = json.load(classes_of_service_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if key == 'LinesOfService' and 'LineOfService' in data:
                    data['LineOfService'] = [{k: v for k, v in lines_of_service.items()
                                               if k in key_values['LineOfService']}
                                              for lines_of_service in data['LineOfService']]
        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self, storage_service, classes_of_service):
        path = '{}{}{}/{}{}/{}'.format(self.root, self.storage_services, storage_service,
                                   self.classes_of_service, classes_of_service, 'index.json')
        try:
            # Read json from file.
            with open(path, 'r') as class_of_service_json:
                data = json.load(class_of_service_json)
                class_of_service_json.close()

            request_data = json.loads(request.data)

            if request_data:
                # Update the keys of payload in json file.
                for key, value in request_data.items():
                    if key in data and data[key]:
                        data[key] = value

            # Write the updated json to file.
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        json_data = self.get(storage_service, classes_of_service)
        return json_data

    def delete(self):
        pass


class ClassOfServiceCollectionAPI(Resource):
    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.classes_of_service = PATHS['StorageServices']['class_of_service']

    def get(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                    self.classes_of_service, 'Index.json')
        print("ClassesOfServiceCollectionAPI--Path---{}".format(path))
        list_of_keys = ['Description', 'Members', 'Name', 'Oem','Permissions']
        key_values = {
	    'Permissions': ['@odata.id'],
            'Members': ['@odata.id', 'ClassOfServiceVersion', 'Description', 'Id', 'Identifier', 'Name', 'Oem',
                        'LinesOfService']
        }
        try:
            classes_of_service_json = open(path)
            data = json.load(classes_of_service_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if key == 'Members' and 'Members' in data:
                    data['Members'] = [{k: v for k, v in member.items()
                                        if k in key_values['Members']}
                                       for member in data['Members']]

        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                   self.classes_of_service, 'Index.json')
        try:
            # Read json from file.
            with open(path, 'r') as class_of_service_json:
                data = json.load(class_of_service_json)
                class_of_service_json.close()

            request_data = json.loads(request.data)

            if request_data:
                # Update the keys of payload in json file.
                for key, value in request_data.items():
                    if key in data and data[key]:

                        data[key] = value

            # Write the updated json to file.
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        json_data = self.get(storage_service)
        return json_data


    def delete(self):
        pass

class DataProtectionLoSCapabilitiesAPI(Resource):

    def __init__(self):
        #print ("sfsfsf")
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.data_protection_los_capabilities = PATHS['StorageServices']['data_protection_los_capabilities']

    def get(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                    self.data_protection_los_capabilities, 'index.json')
        list_of_keys = ['Description', 'Id', 'Identifier', 'Links', 'Name', 'SupportsIsolated', 'SupportedReplicaTypes',
                        'SupportedRecoveryTimeObjectives', 'SupportedRecoveryPointObjectiveSeconds',
                        'SupportedRecoveryGeographicObjectives',
                        'Oem', 'SupportedDataProtectionLinesOfService', 'SupportedMinLifetime','Permissions']
        key_values = {
	           'Permissions': ['@odata.id'],
                'Links': ['SupportedReplicaOptions', 'Oem']

        }
        try:
            data_protection_los_capabilities_json = open(path)
            data = json.load(data_protection_los_capabilities_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if key == 'Links' and 'Links' in data:
                    data['Links'] = [{k: v for k, v in links.items()
                                      if k in key_values['Links']}
                                     for links in data['Links']]


        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                       self.data_protection_los_capabilities, 'index.json')

        try:
            # Read json from file.
            with open(path, 'r') as data_protection_los_capabilities_json:
                data = json.load(data_protection_los_capabilities_json)
                data_protection_los_capabilities_json.close()

            request_data = json.loads(request.data)

            if request_data:
                # Update the keys of payload in json file.
                for key, value in request_data.items():
                    if key in data and data[key]:
                        data[key] = value

            # Write the updated json to file.
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        json_data = self.get(storage_service)
        return json_data

    def delete(self):
        pass

class DataSecurityLoSCapabilitiesAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.data_security_los_capabilities = PATHS['StorageServices']['data_security_los_capabilities']

    def get(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                       self.data_security_los_capabilities, 'index.json')
        list_of_keys = ['Description', 'Id', 'Identifier', 'Name', 'Oem', 'SupportedAntivirusEngineProviders',
                        'SupportedAntivirusScanPolicies', 'SupportedChannelEncryptionStrengths',
                        'SupportedDataSanitizationPolicies'
            , 'SupportedDataSecurityLinesOfService', 'SupportedHostAuthenticationTypes',
                        'SupportedMediaEncryptionStrengths'
            , 'SupportedSecureChannelProtocols', 'SupportedUserAuthenticationTypes','Permissions']
	
	key_values = {
            'Permissions': ['@odata.id']
	}


        try:
            data_security_los_capabilities_json = open(path)
            data = json.load(data_security_los_capabilities_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue


        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                       self.data_security_los_capabilities, 'index.json')

        try:
            # Read json from file.
            with open(path, 'r') as data_security_los_capabilities_json:
                data = json.load(data_security_los_capabilities_json)
                data_security_los_capabilities_json.close()

            request_data = json.loads(request.data)

            if request_data:
                # Update the keys of payload in json file.
                for key, value in request_data.items():
                    if key in data and data[key]:
                        data[key] = value

            # Write the updated json to file.
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        json_data = self.get(storage_service)
        return json_data

    def delete(self):
        pass

class DataStorageLoSCapabilitiesAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.data_storage_los_capabilities = PATHS['StorageServices']['data_storage_los_capabilities']

    def get(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                       self.data_storage_los_capabilities, 'index.json')
        list_of_keys = ['Description', 'Id', 'Identifier', 'Name', 'Oem', 'SupportedAccessCapabilities',
                        'SupportedDataStorageLinesOfService', 'SupportedProvisioningPolicies',
                        'SupportedRecoveryTimeObjectives','SupportsSpaceEfficiency','Permissions']
        key_values = {
            'Permissions': ['@odata.id']
        }
	

        try:
            data_storage_los_capabilities_json = open(path)
            data = json.load(data_storage_los_capabilities_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue


        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                       self.data_storage_los_capabilities, 'index.json')

        try:
            # Read json from file.
            with open(path, 'r') as data_storage_los_capabilities_json:
                data = json.load(data_storage_los_capabilities_json)
                data_storage_los_capabilities_json.close()

            request_data = json.loads(request.data)

            if request_json:
                # Update the keys of payload in json file.
                for key, value in request_data.items():
                    if key in data and data[key]:
                        data[key] = value

            # Write the updated json to file.
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        json_data = self.get(storage_service)
        return json_data

    def delete(self):
        pass


class IOConnectivityLoSCapabilitiesAPI(Resource):
    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.ioconnectivity_los_capabilities = PATHS['StorageServices']['ioconnectivity_los_capabilities']

    def get(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                       self.ioconnectivity_los_capabilities, 'index.json')
        list_of_keys = ['Description', 'Id', 'Identifier', 'MaxSupportedIOPS', 'Name', 'Oem',
                        'SupportedAccessProtocols',
                        'SupportedIOConnectivityLinesOfService','Permissions']
	key_values = {
            'Permissions': ['@odata.id']
	}

        try:
            ioconnectivity_los_capabilities_json = open(path)
            data = json.load(ioconnectivity_los_capabilities_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue



        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                       self.ioconnectivity_los_capabilities, 'index.json')

        try:
            # Read json from file.
            with open(path, 'r') as ioconnectivity_los_capabilities_json:
                data = json.load(ioconnectivity_los_capabilities_json)
                ioconnectivity_los_capabilities_json.close()

            request_data = json.loads(request.data)

            if request_data:
                # Update the keys of payload in json file.
                for key, value in request_data.items():
                    if key in data and data[key]:
                        data[key] = value

            # Write the updated json to file.
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        json_data = self.get(storage_service)
        return json_data

    def delete(self):
        pass


class IOPerformanceLoSCapabilitiesAPI(Resource):
    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.ioperformance_los_capabilities = PATHS['StorageServices']['ioperformance_los_capabilities']

    def get(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                       self.ioperformance_los_capabilities, 'index.json')
        list_of_keys = ['Description', 'Id', 'Identifier', 'IOLimitingIsSupported', 'MaxSamplePeriod',
                        'MinSamplePeriod','MinSupportedIoOperationLatencyMicroseconds', 'Name', 'Oem',
                        'SupportedIOPerformanceLinesOfService','Permissions',
                        'SupportedIOWorkloads']
        key_values = {
		'Permissions': ['@odata.id']
        }
        try:
            ioperformance_los_capabilities_json = open(path)
            data = json.load(ioperformance_los_capabilities_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if key == 'LinesOfService' and 'LinesOfService' in data:
                    data['LinesOfService'] = [{k: v for k, v in lines_of_service.items()
                                               if k in key_values['LinesOfService']}
                                              for lines_of_service in data['LinesOfService']]


        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500
        
        return jsonify(data)

    def put(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                       self.ioperformance_los_capabilities, 'index.json')

        try:
            # Read json from file.
            with open(path, 'r') as ioperformance_los_capabilities_json:
                data = json.load(ioperformance_los_capabilities_json)
                ioperformance_los_capabilities_json.close()

            request_data = json.loads(request.data)

            if request_data:
                # Update the keys of payload in json file.
                for key, value in request_data.items():
                    if key in data and data[key]:
                        data[key] = value

            # Write the updated json to file.
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        json_data = self.get(storage_service)
        return json_data

    def delete(self):
        pass

class StorageSubsystemsAPI(Resource):
    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.storage_subsystems = PATHS['StorageServices']['storage_subsystems']

    def get(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                       self.storage_subsystems, 'index.json')
        list_of_keys = ['Description', 'Id', 'Members','Oem','Name']
        key_values = {
		'Members': ['@odata.id']
        }
        try:
            storage_subsystems_json = open(path)
            data = json.load(storage_subsystems_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                

        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500
        
        return jsonify(data)

    
class VolumesCollectionAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.volumes = PATHS['StorageServices']['volumes']


    def get(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                    self.volumes, 'index.json')
        print("VolumesCollectionAPI--Path---{}".format(path))
        list_of_keys = ['Description', 'Members', 'Name', 'Oem', 'Permissions']
        key_values = {
            'Permissions': ['@odata.id'],
           
            'Members': ['@odata.id', 'AccessCapabilities', 'Actions', 'AllocatedPools', 'BlockSizeBytes', 'Capacity',
                        'CapacityBytes', 'CapacitySources',
                        'Description', 'Encrypted', 'EncryptionTypes', 'Id', 'Identifiers', 'Links',
                        'LowSpaceWarningThresholdPercents', 'Manufacturer',
                        'MaxBlockSizeBytes', 'Model', 'Name', 'Oem', 'Operations', 'ReplicaInfos', 'OptimumIOSizeBytes',
                        'Status', 'StorageGroups',
                        'VolumeType']
        }
        try:
            volumes_json = open(path)
            data = json.load(volumes_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if key == 'Members' and 'Members' in data:
                    data['Members'] = [{k: v for k, v in member.items()
                                        if k in key_values['Members']}
                                       for member in data['Members']]

        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)


    def put(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                       self.volumes, 'index.json')
        try:
            # Read json from file.
            with open(path, 'r') as volumes_json:
                data = json.load(volumes_json)
                volumes_json.close()

            request_data = json.loads(request.data)

            if request_data:
                # Update the keys of payload in json file.
                for key, value in request_data.items():
                    if key in data and data[key]:
                        data[key] = value

            # Write the updated json to file.
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        json_data = self.get(storage_service)
        return json_data


    def delete(self):
        pass


class VolumesAPI(Resource):
    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.volumes = PATHS['StorageServices']['volumes']

    def get(self, storage_service, volumes):
        if volumes == "template":
			path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,

                                       self.volumes, 'volumes_schemaupdate.json')									   
        else:            
            path = '{}{}{}/{}{}/{}'.format(self.root, self.storage_services, storage_service, self.volumes, volumes, 'index.json')
            print path
        list_of_keys = ['AccessCapabilities', 'Actions', 'AllocatedPools', 'BlockSizeBytes', 'Capacity',
                        'CapacityBytes', 'CapacitySources',
                        'Description', 'Encrypted', 'EncryptionTypes', 'Id', 'Identifiers', 'Links',
                        'LowSpaceWarningThresholdPercents',
                        'Manufacturer', 'MaxBlockSizeBytes', 'Model', 'Name', 'Oem', 'Operations', 'OptimumIOSizeBytes',
                        'ReplicaInfos',
                        'Status', 'StorageGroups', 'VolumeType']
        key_values = {
            'Actions': ['Volume.Initialize', 'Oem'],
            'AllocatedPools': ['AllocatedPools', 'AllocatedVolumes', 'BlockSizeBytes', 'Capacity', 'CapacitySources',
                               'ClassesOfService',
                               'Description', 'Id', 'Identifier', 'Links', 'LowSpaceWarningThresholdPercents', 'Name',
                               'Oem', 'Status'],
            'Capacity': ['Data', 'IsThinProvisioned', 'Metadata', 'Snapshots'],
            'CapacitySources': ['ProvidedCapacity', 'ProvidedClassOfService', 'ProvidingDrives', 'ProvidingPools',
                                'ProvidingVolumes','LowSpaceWarningThresholdPercents','Links'],
            'Links': ['ClassOfService', 'Drives', 'Oem'],
            'Operations': ['AssociatedTask', 'OperationName', 'PercentageComplete'],
            'ReplicaInfos': ['ConsistencyEnabled', 'ConsistencyState', 'ConsistencyStatus', 'ConsistencyType',
                             'FailedCopyStopsHostIO',
                             'PercentSynced', 'Replica', 'ReplicaPriority', 'ReplicaProgressStatus',
                             'ReplicaReadOnlyAccess',
                             'ReplicaRecoveryMode', 'ReplicaRole', 'ReplicaSkewBytes', 'ReplicaState', 'ReplicaType',
                             'ReplicaUpdateMode',
                             'RequestedReplicaState', 'SyncMaintained', 'UndiscoveredElement', 'WhenActivated',
                             'WhenDeactivated',
                             'WhenEstablished', 'WhenSuspended', 'WhenSynced', 'WhenSynchronized'],
            'StorageGroups': ['AccessState', 'Actions', 'ClientEndpointGroups', 'Description', 'Id', 'Identifier',
                              'Links', 'MembersAreConsistent',
                              'Name', 'Oem', 'ReplicaInfos', 'ServerEndpointGroups', 'Status', 'Volumes',
                              'VolumesAreExposed']

        }
        try:
            volumes_json = open(path)
            data = json.load(volumes_json)
            #import pdb; pdb.set_trace()
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue

                if key == 'Actions' and 'Actions' in data:
                    data['Actions'] = {k: v for k, v in data['Actions'].items() if k in key_values['Actions']}

                if key == 'Links' and 'Links' in data:
                    data['Links'] = {k: v for k, v in data['Links'].items() if k in key_values['Links']}

                
                if type(data.get('AllocatedPools')) is list:
                    
                    data['AllocatedPools'] = [{k: v for k, v in allocatedpools.items()
                                               if k in key_values['AllocatedPools']}
                                              for allocatedpools in data['AllocatedPools']]
                elif data.get('AllocatedPools'):
                    
                    data['AllocatedPools'] = {k: v for k, v in data['AllocatedPools'].items()
                                               if k in key_values['AllocatedPools']}


                if type(data.get('Capacity')) is list:
                    
                    data['Capacity'] = [{k: v for k, v in capacity.items()
                                               if k in key_values['Capacity']}
                                              for capacity in data['Capacity']]
                             
                elif data.get('Capacity'):
                    
                    data['Capacity'] = {k: v for k, v in data['Capacity'].items()
                                               if k in key_values['Capacity']}

                if key == 'CapacitySources' and 'CapacitySources' in data:
                    data['CapacitySources'] = [{k: v for k, v in capacity_sources.items()
                                               if k in key_values['CapacitySources']}
                                              for capacity_sources in data['CapacitySources']]

                if key == 'Operations' and 'Operations' in data:
                    data['Operations'] = {k: v for k, v in data['Operations'].items() if k in key_values['Operations']}

                
                if key == 'ReplicaInfos' and 'ReplicaInfos' in data:
                    data['ReplicaInfos'] = [{k: v for k, v in replica_infos.items()
                                               if k in key_values['ReplicaInfos']}
                                              for replica_infos in data['ReplicaInfos']]
                
                if type(data.get('StorageGroups')) is list:
                    
                    data['StorageGroups'] = [{k: v for k, v in storagegroups.items()
                                               if k in key_values['StorageGroups']}
                                              for storagegroups in data['StorageGroups']]
                elif data.get('StorageGroups'):
                    
                    data['StorageGroups'] = {k: v for k, v in data['StorageGroups'].items()
                                               if k in key_values['StorageGroups']}


        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self, storage_service, volumes):
        path = '{}{}{}/{}{}/{}'.format(self.root, self.storage_services, storage_service,
                                       self.volumes, volumes, 'index.json')
        try:
            # Read json from file.
            with open(path, 'r') as volumes_json:
                data = json.load(volumes_json)
                volumes_json.close()

            request_data = json.loads(request.data)

            if request_data:
                # Update the keys of payload in json file.
                for key, value in request_data.items():
                    if key in data and data[key]:
                        data[key] = value

            # Write the updated json to file.
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        json_data = self.get(storage_service, volumes)
        return json_data

	
    def post(self, storage_service, volumes):
        #create folder  
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                           self.volumes, volumes)
        try:
            os.mkdir(path)
            #data = urllib2.urlopen("http://redfish.dmtf.org/schemas/swordfish/v1/Volume.v1_1_0.json")
            
            data = json.loads(request.data)
            with open(path+"/index.json", "w") as fd:
                json.dump(data, fd)
            
            # add entry of new filesystem
            
            modifieddata = {}
            with open(path+"/../index.json") as pdata:
                modifieddata = json.loads(pdata.read())
                modifieddata["Members"].append({"@odata.id":modifieddata["@odata.id"]+"/"+volumes})
                
            with open(path+"/../index.json","w") as volumes_json:  
             #   print "in write",pdata            
                json.dump(modifieddata, volumes_json)
               
            return modifieddata
        except Exception as e:
             return {"error": "Unable create file because of following error::{}".format(e)}, 500    



    def delete(self):
        pass

class VolumesChildAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.volumes = PATHS['StorageServices']['volumes']

    def get(self, storage_service, volumes, values):
        path = '{}{}{}/{}{}/{}/{}'.format(self.root, self.storage_services, storage_service,
                                       self.volumes, volumes, values, 'index.json')

        try:
            volumes_json = open(path)
            data = json.load(volumes_json)
        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)




class EndpointsCollectionAPI(Resource):
    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.endpoints = PATHS['StorageServices']['endpoints']

    def get(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                    self.endpoints, 'index.json')
        print("EndpointsCollectionAPI--Path---{}".format(path))
        list_of_keys = ['Description', 'Members', 'Name', 'Oem','Permissions']
        key_values = {
	    'Permissions': ['@odata.id'],
            'Members': ['@odata.id']
        }
        try:
            endpoints_json = open(path)
            data = json.load(endpoints_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if key == 'Members' and 'Members' in data:
                    data['Members'] = [{k: v for k, v in member.items()
                                        if k in key_values['Members']}
                                       for member in data['Members']]

        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self):
        pass

    def delete(self):
        pass


class EndpointsAPI(Resource):
    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.endpoints = PATHS['StorageServices']['endpoints']

    def get(self, storage_service, endpoints):
        path = '{}{}{}/{}{}/{}'.format(self.root, self.storage_services, storage_service,
                                       self.endpoints, endpoints, 'index.json')
        list_of_keys = ['AccessState', 'Description', 'Endpoints', 'GroupType', 'Id', 'Identifier', 'Links', 'Name',
                        'Oem', 'Preferred', 'TargetEndpointGroupIdentifier']
        key_values = {
            'Endpoints': ['Description', 'Members', 'Name', 'Oem'],
            'Links': ['Oem']
        }
        try:
            endpoints_json = open(path)
            data = json.load(endpoints_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if key == 'Endpoints' and 'Endpoints' in data:
                    data['Endpoints'] = [{k: v for k, v in endpoints.items()
                                          if k in key_values['Endpoints']}
                                         for endpoints in data['Endpoints']]
                if key == 'Links' and 'Links' in data:
                    data['Links'] = [{k: v for k, v in links.items()
                                      if k in key_values['Links']}
                                     for links in data['Links']]


        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self):
        pass

    def delete(self):
        pass


class FileSystemsCollectionAPI(Resource):
    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.file_systems = PATHS['StorageServices']['file_systems']

    def get(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                    self.file_systems, 'index.json')
        print("FileSystemsCollectionAPI--Path---{}".format(path))
        list_of_keys = ['Description', 'Members', 'Name', 'Oem', 'Permissions']
        key_values = {
	    'Permissions': ['@odata.id'],
            'Members': ['@odata.id', 'AccessCapabilities', 'BlockSizeBytes', 'Capacity', 'CapacitySources',
                        'CasePreserved',
                        'CaseSensitive', 'CharacterCodeSet', 'ClusterSizeBytes', 'Description', 'ExportedShares', 'Id',
                        'Links',
                        'LowSpaceWarningThresholdPercents', 'MaxFileNameLengthBytes', 'Name', 'Oem',
                        'RemainingCapacity', 'ReplicaInfo','definitions']
        }
        try:
            file_systems_json = open(path)
            data = json.load(file_systems_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if key == 'Members' and 'Members' in data:
                    data['Members'] = [{k: v for k, v in member.items()
                                        if k in key_values['Members']}
                                       for member in data['Members']]

        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self, storage_service):
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                       self.file_systems, 'index.json')
        try:
            # Read json from file.
            with open(path, 'r') as file_systems_json:
                data = json.load(file_systems_json)
                file_systems_json.close()

            request_data = json.loads(request.data)

            if request_data:
                # Update the keys of payload in json file.
                for key, value in request_data.items():
                    if key in data and data[key]:
                        data[key] = value

            # Write the updated json to file.
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        json_data = self.get(storage_service)
        return json_data

    def delete(self):
        pass
class FileSystemsChildAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.file_systems = PATHS['StorageServices']['file_systems']

    def get(self, storage_service, file_systems, values):
        path = '{}{}{}/{}{}/{}/{}'.format(self.root, self.storage_services, storage_service,
                                       self.file_systems, file_systems, values, 'index.json')

        try:
            file_systems_json = open(path)
            data = json.load(file_systems_json)
        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)
		
		

class FileSystemsAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']
        self.storage_services = PATHS['StorageServices']['path']
        self.file_systems = PATHS['StorageServices']['file_systems']

    def get(self, storage_service, file_systems):
        if file_systems == "template":
			path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,

                                       self.file_systems, 'filesystems_schemaupdate.json')
									   
        else:
            
            path = '{}{}{}/{}{}/{}'.format(self.root, self.storage_services, storage_service, self.file_systems, file_systems, 'index.json')
            print path


        list_of_keys = ['AccessCapabilities', 'BlockSizeBytes', 'Capacity', 'CapacitySources', 'CasePreserved',
                        'CaseSensitive',
                        'CharacterCodeSet', 'ClusterSizeBytes', 'Description', 'ExportedShares', 'Id', 'Links',
                        'LowSpaceWarningThresholdPercents', 'MaxFileNameLengthBytes', 'Name', 'Oem',
                        'RemainingCapacity', 'ReplicaInfo']
        key_values = {
            'Capacity': ['Data', 'IsThinProvisioned', 'Metadata', 'Snapshot'],
            'CapacitySources': ['ProvidedCapacity', 'ProvidedClassOfService', 'ProvidingDrives', 'ProvidingPools',
                                'ProvidingVolumes','LowSpaceWarningThresholdPercents'],
            'ExportedShares': ['CASupported', 'DefaultAccessPrivileges', 'Description', 'EthernetInterfaces',
                               'ExecuteSupport',
                               'FileSharePath', 'FileShareQuotaType', 'FileShareRemainingQuotaBytes',
                               'FileShareTotalQuotaBytes',
                               'FileSharingProtocols', 'Id', 'Links', 'LowSpaceWarningThresholdPercents', 'Name', 'Oem',
                               'RootAccess',
                               'Status', 'WritePolicy'],
            'Links': ['ClassOfService', 'Oem', 'ReplicaCollection'],
            'RemainingCapacity': ['Data', 'IsThinProvisioned', 'Metadata', 'Snapshot'],
            'ReplicaInfo': ['ConsistencyEnabled', 'ConsistencyState', 'ConsistencyStatus', 'ConsistencyType',
                            'FailedCopyStopsHostIO',
                            'PercentSynced', 'Replica', 'ReplicaPriority', 'ReplicaProgressStatus',
                            'ReplicaReadOnlyAccess',
                            'ReplicaRecoveryMode', 'ReplicaRole', 'ReplicaSkewBytes', 'ReplicaState', 'ReplicaType',
                            'ReplicaUpdateMode',
                            'RequestedReplicaState', 'SyncMaintained', 'UndiscoveredElement', 'WhenActivated',
                            'WhenDeactivated',
                            'WhenEstablished', 'WhenSuspended', 'WhenSynced', 'WhenSynchronized']

        }
        try:
            file_systems_json = open(path)
            data = json.load(file_systems_json)
            for key, value in data.items():
                if key not in list_of_keys:
                    del data[key]
                    continue
                if type(data.get('Capacity')) is list:
                    
                    data['Capacity'] = [{k: v for k, v in capacity.items()
                                               if k in key_values['Capacity']}
                                              for capacity in data['Capacity']]
                             
                elif data.get('Capacity'):
                    
                    data['Capacity'] = {k: v for k, v in data['Capacity'].items()
                                               if k in key_values['Capacity']}
                if key == 'CapacitySources' and 'CapacitySources' in data:
                    data['CapacitySources'] = [{k: v for k, v in capacity_sources.items()
                                                if k in key_values['CapacitySources']}
                                               for capacity_sources in data['CapacitySources']]
                if key == 'Links' and 'Links' in data:
                    data['Links'] = [{k: v for k, v in links.items()
                                      if k in key_values['Links']}
                                     for links in data['Links']]
                
                if type(data.get('ExportedShares')) is list:
                    
                    data['ExportedShares'] = [{k: v for k, v in exportedshares.items()
                                               if k in key_values['ExportedShares']}
                                              for exportedshares in data['ExportedShares']]
                             
                elif data.get('ExportedShares'):
                    
                    data['ExportedShares'] = {k: v for k, v in data['ExportedShares'].items()
                                               if k in key_values['ExportedShares']}

                if key == 'ExportedShares' and 'ExportedShares' in data:
                    data['ExportedShares'] = [{k: v for k, v in exported_shares.items()
                                               if k in key_values['ExportedShares']}
                                              for exported_shares in data['ExportedShares']]
                if key == 'RemainingCapacity' and 'RemainingCapacity' in data:
                    data['RemainingCapacity'] = [{k: v for k, v in remaining_capacity.items()
                                                  if k in key_values['RemainingCapacity']}
                                                 for remaining_capacity in data['RemainingCapacity']]
                if key == 'ReplicaInfo' and 'ReplicaInfo' in data:
                    data['ReplicaInfo'] = [{k: v for k, v in replica_info.items()
                                            if k in key_values['ReplicaInfo']}
                                           for replica_info in data['ReplicaInfo']]


        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    def put(self, storage_service, file_systems):
        path = '{}{}{}/{}{}/{}'.format(self.root, self.storage_services, storage_service,
                                       self.file_systems, file_systems, 'index.json')
        try:
            # Read json from file.
            with open(path, 'r') as file_systems_json:
                data = json.load(file_systems_json)
                file_systems_json.close()

            request_data = json.loads(request.data)

            if request_data:
                # Update the keys of payload in json file.
                for key, value in request_data.items():
                    if key in data and data[key]:
                        data[key] = value

            # Write the updated json to file.
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        json_data = self.get(storage_service, file_systems)
        return json_data

    def post(self, storage_service, file_systems):
        #create folder  
        path = '{}{}{}/{}{}'.format(self.root, self.storage_services, storage_service,
                                           self.file_systems, file_systems)
        try:
            os.mkdir(path)
            #data = urllib2.urlopen("http://redfish.dmtf.org/schemas/swordfish/v1/FileSystem.v1_0_0.json")
            
            data = json.loads(request.data)
            with open(path+"/index.json", "w") as fd:
                json.dump(data, fd)
            
            # add entry of new filesystem
            
            modifieddata = {}
            with open(path+"/../index.json") as pdata:
                modifieddata = json.loads(pdata.read())
                modifieddata["Members"].append({"@odata.id":modifieddata["@odata.id"]+"/"+file_systems})
                
            with open(path+"/../index.json","w") as file_systems_json:  
             #   print "in write",pdata            
                json.dump(modifieddata, file_systems_json)
               
            return modifieddata
        except Exception as e:
             return {"error": "Unable create file because of following error::{}".format(e)}, 500

    def delete(self):
        pass




