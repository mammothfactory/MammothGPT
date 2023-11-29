from datasets import DatasetBuilder, SplitGenerator, GeneratorBasedBuilder, Split, DatasetInfo
from datasets.features import Features, Value



class ParcelSummaryDataset(GeneratorBasedBuilder):
    
    VERSION = "1.0.0"
    #BUILDER_CONFIG_CLASS = GeneratorBasedBuilder

    def _info(self):
        return DatasetInfo(description="qPublic Owener and Parcel Summary", features=Features({
            'contactNames': Value('string'),
            'parcelId': Value('string'),
            'parcelAddress': Value('string'),
            'description': Value('string'),
            'propertyUseCode': Value('string'),
            'acreage': Value('string'),
            'homestead': Value('string'),
            'link': Value('string'),           
        }),
        )
        
    def _split_generators(self, dl_manager):
        downloaded_file = dl_manager.download_and_extract("https://huggingface.co/datasets/mammoth-blaze/ParcelSummaryDS/raw/main/ParcelSummaryDS.py")
        
        return [
            SplitGenerator(name=Split.TRAIN, gen_kwargs={"filepath": downloaded_file}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            for idx, line in enumerate(f):
                contactNames, parcelId, parcelAddress, description, propertyUseCode, acreage, homestead, link = line.strip().split('\t')
                yield idx, {"contactNames": contactNames, "parcelId": parcelId, "parcelAddress": parcelAddress, "description": description, "propertyUseCode": propertyUseCode, "acreage": acreage, "homestead": homestead, "link": link}
