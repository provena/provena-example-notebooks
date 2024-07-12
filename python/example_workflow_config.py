from pydantic import BaseModel
import json
from provenaclient import ProvenaClient


class ModelOutputs(BaseModel):
    # This is a key part of the model run configuration - it specifies a set of
    # expected dataset references - the value here should be the handle
    # identifier of the Provena registered Dataset

    output_dataset: str
    output_dataset_template: str

    async def validate_entities(self, client: ProvenaClient) -> bool:
        print("Validating registered output datasets...")

        datasets = [
            self.output_dataset
        ]

        templates = [
            self.output_dataset_template
        ]

        for id in datasets:
            try:
                await client.datastore.fetch_dataset(id=id)
            except Exception as e:
                print(
                    f"Encountered exception while validating Dataset: {id=}. Exception: {e}.")
                return False

        for id in templates:
            try:
                await client.registry.dataset_template.fetch(id=id)
            except Exception as e:
                print(
                    f"Encountered exception while validating Dataset Template: {id=}. Exception: {e}.")
                return False

        return True


class ModelInputs(BaseModel):
    # This is a key part of the model run configuration - it specifies a set of
    # expected dataset references - the value here should be the handle
    # identifier of the Provena registered Dataset

    # each part includes the template ID and the dataset ID which matches it

    # The hourly temperature dataset - i.e.
    # nbic.catalog_s3_stage1.weather.projected.to_path('AU_input_dataset_C.zarr')
    input_dataset: str
    input_dataset_template: str


    async def validate_entities(self, client: ProvenaClient) -> bool:

        datasets = [
            self.input_dataset            
        ]

        templates = [
            self.input_dataset_template            
        ]

        for id in datasets:
            print("in loop.")
            try:
                print("in here.")
                model = await client.datastore.fetch_dataset(id=id)
                print(model)
            except Exception as e:
                print(
                    f"Encountered exception while validating Dataset: {id=}. Exception: {e}.")
                return False

        for id in templates:
            try:
                await client.registry.dataset_template.fetch(id=id)
            except Exception as e:
                print(
                    f"Encountered exception while validating Dataset Template: {id=}. Exception: {e}.")
                return False

        return True


class ModelAssociations(BaseModel):
    # This links the model run to a user/organisation

    # registered Person
    person: str

    # registered organisation
    organisation: str

    async def validate_entities(self, client: ProvenaClient) -> bool:
        print("Validating registered associations...")

        people = [
            self.person
        ]

        organisations = [
            self.organisation
        ]

        for id in people:
            try:
                await client.registry.person.fetch(id=id)
            except Exception as e:
                print(
                    f"Encountered exception while validating Person: {id=}. Exception: {e}.")
                return False

        for id in organisations:
            try:
                await client.registry.organisation.fetch(id=id)
            except Exception as e:
                print(
                    f"Encountered exception while validating Organisation: {id=}. Exception: {e}.")
                return False

        return True


class ModelConfigurationEntities(BaseModel):
    # The registered model run workflow template
    workflow_template: str

    async def validate_entities(self, client: ProvenaClient) -> bool:
        print("Validating registered associations...")

        wf_templates = [
            self.workflow_template
        ]

        for id in wf_templates:
            try:
                await client.registry.model_run_workflow.fetch(id=id)
            except Exception as e:
                print(
                    f"Encountered exception while validating Model Run Workflow Template: {id=}. Exception: {e}.")
                return False

        return True


class HourlyJYIWorkflowConfig(BaseModel):
    inputs: ModelInputs
    outputs: ModelOutputs
    associations: ModelAssociations
    workflow_configuration: ModelConfigurationEntities

    def pprint(self) -> None:
        print(json.dumps(json.loads(self.json()), indent=2))

    @staticmethod
    def dump_example(path: str) -> None:
        empty_example = HourlyJYIWorkflowConfig(
            inputs=ModelInputs(
                input_dataset="TODO"                
            ),
            outputs=ModelOutputs(
                output_dataset="TODO",
                output_dataset_template="TODO"
            ),
            associations=ModelAssociations(
                person="TODO",
                organisation="TODO"
            ),
            workflow_configuration=ModelConfigurationEntities(
                workflow_template="TODO"
            )
        )

        json_content = json.dumps(json.loads(empty_example.json()), indent=2)
        with open(path, 'w') as f:
            f.write(json_content)

    async def validate_entities(self, client: ProvenaClient) -> bool:
        print("Validating registered Provena entities in config")

        inputs = await self.inputs.validate_entities(
            client = client
        )

        if not inputs:
            print("Failed inputs validation.")
            return False

        outputs = await self.outputs.validate_entities(
            client = client)

        if not outputs:
            print("Failed outputs validation.")
            return False

        associations = await self.associations.validate_entities(
            client = client)

        if not associations:
            print("Failed associations validation.")
            return False

        model_config = await self.workflow_configuration.validate_entities(
            client = client)

        if not model_config:
            print("Failed workflow configuration validation.")
            return False

        print("Validation successful...")
        return True


def load_config(path: str) -> HourlyJYIWorkflowConfig:
    """

    Loads the config from the specific path. 

    This should be a JSON file which satisfies the model above.

    Args:
        path (str): The file path.

    Raises:
        Exception: Failed loading file/parsing

    Returns:
        HourlyFFDIWorkflowConfig: The parsed config object
    """

    try:
        return HourlyJYIWorkflowConfig.parse_file(path=path)
    except Exception as e:
        raise Exception(
            f"An exception occurred when loading config from {path = }. Exception: {e}.")


if __name__ == "__main__":
    HourlyJYIWorkflowConfig.dump_example(path="configs/template.json")
