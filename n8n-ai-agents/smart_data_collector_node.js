/**
 * Smart Data Collector Node for n8n
 * Collects data from multiple sources with AI-powered filtering
 */

const { IExecuteFunctions, INodeExecutionData, INodeType, INodeTypeDescription } = require('n8n-workflow');
const axios = require('axios');

class SmartDataCollector implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'Smart Data Collector',
        name: 'smartDataCollector',
        icon: 'fa:database',
        group: ['input'],
        version: 1,
        subtitle: '={{$parameter["source"]}}',
        description: 'Collect and filter data from multiple sources using AI',
        defaults: {
            name: 'Smart Data Collector',
        },
        inputs: ['main'],
        outputs: ['main'],
        credentials: [
            {
                name: 'newsApiCredentials',
                required: false,
            },
            {
                name: 'twitterApiCredentials',
                required: false,
            },
        ],
        properties: [
            {
                displayName: 'Data Source',
                name: 'source',
                type: 'options',
                noDataExpression: true,
                options: [
                    {
                        name: 'News Articles',
                        value: 'news',
                        description: 'Collect news articles from various sources',
                    },
                    {
                        name: 'Social Media',
                        value: 'social',
                        description: 'Collect social media posts and comments',
                    },
                    {
                        name: 'Reddit Posts',
                        value: 'reddit',
                        description: 'Collect Reddit posts and discussions',
                    },
                    {
                        name: 'Product Reviews',
                        value: 'reviews',
                        description: 'Collect product reviews and ratings',
                    },
                    {
                        name: 'All Sources',
                        value: 'all',
                        description: 'Collect from all available sources',
                    },
                ],
                default: 'news',
            },
            {
                displayName: 'Search Query',
                name: 'query',
                type: 'string',
                default: '',
                placeholder: 'AI technology',
                description: 'Search query to filter relevant content',
                required: true,
            },
            {
                displayName: 'Max Results',
                name: 'maxResults',
                type: 'number',
                default: 10,
                description: 'Maximum number of results to collect',
                typeOptions: {
                    minValue: 1,
                    maxValue: 100,
                },
            },
            {
                displayName: 'AI Filtering',
                name: 'aiFiltering',
                type: 'boolean',
                default: true,
                description: 'Use AI to filter and rank results by relevance',
            },
            {
                displayName: 'Sentiment Filter',
                name: 'sentimentFilter',
                type: 'options',
                options: [
                    {
                        name: 'All',
                        value: 'all',
                        description: 'Include all sentiment types',
                    },
                    {
                        name: 'Positive Only',
                        value: 'positive',
                        description: 'Only positive sentiment content',
                    },
                    {
                        name: 'Negative Only',
                        value: 'negative',
                        description: 'Only negative sentiment content',
                    },
                    {
                        name: 'Neutral Only',
                        value: 'neutral',
                        description: 'Only neutral sentiment content',
                    },
                ],
                default: 'all',
                displayOptions: {
                    show: {
                        aiFiltering: [true],
                    },
                },
            },
            {
                displayName: 'Language',
                name: 'language',
                type: 'options',
                options: [
                    {
                        name: 'English',
                        value: 'en',
                    },
                    {
                        name: 'Spanish',
                        value: 'es',
                    },
                    {
                        name: 'French',
                        value: 'fr',
                    },
                    {
                        name: 'German',
                        value: 'de',
                    },
                    {
                        name: 'Any',
                        value: 'any',
                    },
                ],
                default: 'en',
            },
            {
                displayName: 'Include Metadata',
                name: 'includeMetadata',
                type: 'boolean',
                default: true,
                description: 'Include source metadata (author, date, engagement)',
            },
        ],
    };

    async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
        const items = this.getInputData();
        const returnData: INodeExecutionData[] = [];

        const source = this.getNodeParameter('source', 0) as string;
        const query = this.getNodeParameter('query', 0) as string;
        const maxResults = this.getNodeParameter('maxResults', 0) as number;
        const aiFiltering = this.getNodeParameter('aiFiltering', 0) as boolean;
        const sentimentFilter = this.getNodeParameter('sentimentFilter', 0) as string;
        const language = this.getNodeParameter('language', 0) as string;
        const includeMetadata = this.getNodeParameter('includeMetadata', 0) as boolean;

        try {
            const collectedData = await this.collectData(
                source,
                query,
                maxResults,
                language
            );

            let processedData = collectedData;

            if (aiFiltering) {
                processedData = await this.applyAIFiltering(
                    processedData,
                    sentimentFilter
                );
            }

            for (const item of processedData) {
                const outputItem: any = {
                    content: item.content,
                    title: item.title || '',
                    source: item.source,
                    url: item.url || '',
                    collected_at: new Date().toISOString(),
                };

                if (includeMetadata) {
                    outputItem.metadata = {
                        author: item.author || '',
                        published_date: item.published_date || '',
                        engagement: item.engagement || {},
                        sentiment: item.sentiment || null,
                        confidence: item.confidence || null,
                    };
                }

                returnData.push({ json: outputItem });
            }

        } catch (error) {
            if (this.continueOnFail()) {
                returnData.push({
                    json: {
                        error: error.message,
                        query: query,
                        source: source,
                    },
                });
            } else {
                throw error;
            }
        }

        return [returnData];
    }

    private async collectData(
        source: string,
        query: string,
        maxResults: number,
        language: string
    ): Promise<any[]> {
        const apiEndpoint = 'http://localhost:8082/api';
        
        const response = await axios.post(`${apiEndpoint}/collect_data`, {
            source: source,
            query: query,
            max_results: maxResults,
            language: language,
        });

        return response.data.items || [];
    }

    private async applyAIFiltering(
        data: any[],
        sentimentFilter: string
    ): Promise<any[]> {
        if (sentimentFilter === 'all') {
            return data;
        }

        const apiEndpoint = 'http://localhost:8082/api';
        
        const response = await axios.post(`${apiEndpoint}/filter_by_sentiment`, {
            items: data,
            sentiment_filter: sentimentFilter,
        });

        return response.data.filtered_items || [];
    }
}

module.exports = { nodeClass: SmartDataCollector };